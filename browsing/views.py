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


class TestRDFLibView(GenericListView):
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
        DC = Namespace("http://purl.org/dc/elements/1.1/")
        g.bind('dc', DC)
        for obj in Edition.objects.all():
            edition = URIRef(obj.url)
            title = Literal(obj.name)
            # g.add((RDF.Description, RDF.about, edition))
            g.add((edition, DC.title, title))
            for x in obj.language.all():
                language = Literal(x.iso_code)
                g.add((edition, DC.language, language))
            for x in obj.historical_period.all():
                historical_period = Literal(x.name)
                g.add((edition, DC.coverage, historical_period))
            if obj.begin_date and obj.end_date:
                date = Literal(str(obj.begin_date.strftime("%Y"))+' - '+str(obj.end_date.strftime("%Y")))
                g.add((edition, DC.date, date))
            elif obj.begin_date:
                date = Literal(str(obj.begin_date.strftime("%Y")))
                g.add((edition, DC.date, date))
            elif obj.end_date:
                date = Literal(str(obj.end_date.strftime("%Y")))
                g.add((edition, DC.date, date))
            else:
                pass
            for x in obj.institution.all():
                publisher = Literal(x.name)
                g.add((edition, DC.publisher, publisher))
            for x in obj.manager.all():
                creator = Literal(x.name)
                g.add((edition, DC.creator, creator))
            for x in obj.holding_repo.all():
                source = Literal(x.name)
                g.add((edition, DC.source, source))
            if obj.tei_transcription == "0.5":
                dcformat = Literal("text/xml")
                #this is tricky due to that rdflib takes 'format' for built-in python method and throws an error,
                #found this example http://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html#an-example
                #tried and it worked to fix the error 
                g.add((edition, DC['format'], dcformat))
            elif obj.tei_transcription == "1":
                dcformat = Literal("application/tei+xml")
                g.add((edition, DC['format'], dcformat))
            else:
                pass
            rights = Literal(obj.get_open_source_display())
            g.add((edition, DC.rights, rights))
            identifier = URIRef("https://dig-ed-cat.acdh.oeaw.ac.at/editions/detail/"+str(obj.legacy_id))
            g.add((edition, DC.identifier, identifier))
        result = g.serialize(destination=response, format='pretty-xml')
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
