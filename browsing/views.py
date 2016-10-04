from django.shortcuts import render
from django_tables2 import SingleTableView, RequestConfig
from editions.models import *
from places.models import *
from .filters import EditionListFilter
from .forms import GenericFilterFormHelper
from .tables import EditionTable


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
        edition_names = []
        infrastructure_names = []
        audience_names = []
        writing_support_names = []
        for edition in Edition.objects.all():
            edition_names.append(edition.name)
            infrastructure_names.append(edition.infrastructure)
            audience_names.append(edition.audience)
            writing_support_names.append(edition.writing_support)
        context["edition_names"] = set(edition_names)
        context["infrastructure_names"] = set(infrastructure_names)
        context["audience_names"] = set(audience_names)
        context["writing_support_names"] = set(writing_support_names)
        manager_names = []
        for person in Person.objects.all():
            manager_names.append(person.name)
        context["manager_names"] = set(manager_names)
        institution_names = []
        for inst in Institution.objects.all():
            institution_names.append(inst.name)
        context["institution_names"] = set(institution_names)
        return context


# class InstitutionListView(GenericListView):
#  	model = Place
#  	table_class = InstitutionTable
#  	template_name = 'browsing/place_list_generic.html'
#  	filter_class = InstitutionListFilter
#  	formhelper_class = GenericFilterFormHelper
