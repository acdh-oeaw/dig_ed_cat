import csv
import time
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import SingleTableView, RequestConfig
from editions.models import *
from places.models import *
from .filters import EditionListFilter
from .forms import GenericFilterFormHelper, MapFilterFormHelper
from .tables import EditionTable
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from rdflib.namespace import DC, FOAF, RDFS
from rdflib.namespace import SKOS


def serialize(modelclass):
    fields = modelclass._meta.get_fields()
    serialized = []
    for x in fields:
        if x.get_internal_type() == "ManyToManyField":
            attrs = getattr(modelclass, x.name)
            values = "|".join([y[1] for y in attrs.values_list()])
            key_value = values
        else:
            key_value = getattr(modelclass, x.name)
        serialized.append(key_value)
    return serialized


class GenericListView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    paginate_by = 25

    def get_queryset(self, **kwargs):
        qs = super(GenericListView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        if self.request.GET.get('amount') is not None:
            nr_of_rows = self.request.GET.get('amount')
        else:
            nr_of_rows = 25
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': nr_of_rows}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


class EditionDownloadView(GenericListView):
    model = Edition
    table_class = EditionTable
    template_name = 'browsing/edition_list_generic.html'
    filter_class = EditionListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='text/csv')
        filename = "editions_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        writer = csv.writer(response, delimiter=",")
        writer.writerow([x.name for x in Edition._meta.get_fields()])
        for x in self.get_queryset():
            row = serialize(x)
            writer.writerow(row)
        return response


def EditionXMLView(request):
    response = render_to_response('browsing/xml_template.xml', {'editions': Edition.objects.all(),})
    response['Content-Type'] = 'application/xml; charset=utf-8'
    return response


def EditionBibtextView(request):
    response = render_to_response('browsing/bibtex_template.txt', {'editions': Edition.objects.all(),})
    response['Content-Type'] = 'text/plain; charset=utf-8'
    return response


class EditionRDFView(GenericListView):
    model = Edition
    table_class = EditionTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = EditionListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "editions_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = rdflib.Graph()
        DCAT = Namespace("http://www.w3.org/ns/dcat#")
        DCT = Namespace("http://dublincore.org/documents/dcmi-terms/")
        FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        GEO = Namespace("https://www.w3.org/2003/01/geo/")
        GN = Namespace("http://www.geonames.org/ontology#")
        WGS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
        g.bind('dcat', DCAT)
        g.bind('dct', DCT)
        g.bind('foaf', FOAF)
        g.bind('geo', GEO)
        g.bind('gn', GN)
        g.bind('wgs', WGS)
        for obj in self.get_queryset():
            edition = URIRef("https://dig-ed-cat.acdh.oeaw.ac.at/editions/detail/"+str(obj.legacy_id))
            title = Literal(obj.name)
            g.add((edition, RDF.type, DCAT.Dataset))
            g.add((edition, DCT.title, title))
            for x in obj.language.all():
                language = Literal(x.iso_code)
                g.add((edition, DCT.language, language))
            for x in obj.historical_period.all():
                historical_period = Literal(x.name)
                g.add((edition, DCT.temporal, historical_period))
            if obj.begin_date and obj.end_date:
                date = Literal(str(obj.begin_date.strftime("%Y"))+' - '+str(obj.end_date.strftime("%Y")))
                g.add((edition, DCT.date, date))
            elif obj.begin_date:
                date = Literal(str(obj.begin_date.strftime("%Y")))
                g.add((edition, DCT.date, date))
            elif obj.end_date:
                date = Literal(str(obj.end_date.strftime("%Y")))
                g.add((edition, DCT.date, date))
            else:
                pass
            for x in obj.institution.all():
                publisher = URIRef("#cde/institution/"+str(x.id))
                g.add((edition, DCT.publisher, publisher))
                
                name = Literal(x.name)
                g.add((publisher, RDF.type, FOAF.Organization))
                g.add((publisher, FOAF.name, name))
                homepage = URIRef(x.website)
                g.add((publisher, FOAF.homepage, homepage))
                if x.lat or x.lng:
                    geo_lat = Literal(x.lat)
                    geo_long = Literal(x.lng)
                    g.add((publisher, GEO.lat, geo_lat))
                    g.add((publisher, GEO.long, geo_long))
                if x.gnd_id:
                    seeAlso = URIRef(x.gnd_id)
                    g.add((publisher, RDFS.seeAlso, seeAlso))
                if x.place:
                    g.add((publisher, FOAF.based_near, URIRef("http://sws.geonames.org/"+str(x.place.geonames_id))))
                    based_near = URIRef("http://sws.geonames.org/"+str(x.place.geonames_id))
                    gn_name = Literal(x.place.name)
                    g.add((based_near, RDF.type, GN.Feature))
                    g.add((based_near, RDF.type, GEO.SpatialThing))
                    g.add((based_near, GN.name, gn_name))
                    wgs_lat = Literal(x.place.lat)
                    g.add((based_near, WGS.lat, wgs_lat))
                    wgs_long = Literal(x.place.lng)
                    g.add((based_near, WGS.long, wgs_long))
                    parent_feature = URIRef("http://sws.geonames.org/"+str(x.place.part_of.geonames_id))
                    g.add((based_near, GN.parentFeature, parent_feature))
            for x in obj.manager.all():
                creator = Literal(x.name)
                g.add((edition, DCT.creator, creator))
            for x in obj.holding_repo.all():
                source = Literal(x.name)
                g.add((edition, DCT.source, source))
            if obj.tei_transcription == "0.5":
                dctformat = Literal("text/xml")
                #this is tricky due to that rdflib takes 'format' for built-in python method and throws an error,
                #found this example http://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html#an-example
                #tried and it worked to fix the error 
                g.add((edition, DCT['format'], dctformat))
            elif obj.tei_transcription == "1":
                dctformat = Literal("application/tei+xml")
                g.add((edition, DCT['format'], dctformat))
            else:
                pass
            rights = Literal(obj.get_open_source_display())
            g.add((edition, DCT.rights, rights))
            landingPage = URIRef(obj.url)
            g.add((edition, DCAT.landingPage, landingPage))
            identifier = URIRef("https://dig-ed-cat.acdh.oeaw.ac.at/editions/detail/"+str(obj.legacy_id))
            g.add((edition, DCT.identifier, identifier))
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class EditionListView(GenericListView):
    model = Edition
    table_class = EditionTable
    template_name = 'browsing/edition_list_generic.html'
    filter_class = EditionListFilter
    formhelper_class = GenericFilterFormHelper

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['snyc_log'] = SyncLog.objects.last()
        return context


class MapView(EditionListView):
    template_name = 'browsing/mapview.html'
    filter_class = EditionListFilter
    formhelper_class = MapFilterFormHelper

    def get_context_data(self, **kwargs):
        context = super(EditionListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['snyc_log'] = SyncLog.objects.last()
        institutions = []
        for x in self.get_queryset():
            for y in x.institution.all():
                try:
                    y.place.lat
                    institutions.append(y)
                except:
                    pass
        context["institutions"] = set(institutions)
        return context
