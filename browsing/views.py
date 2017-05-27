from django.shortcuts import render
from django_tables2 import SingleTableView, RequestConfig
from editions.models import *
from places.models import *
from .filters import EditionListFilter
from .forms import GenericFilterFormHelper, MapFilterFormHelper
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
        return context


class MapView(EditionListView):
    template_name = 'browsing/mapview.html'
    filter_class = EditionListFilter
    formhelper_class = MapFilterFormHelper

    def get_queryset(self, **kwargs):
        qs = Edition.objects.all()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(EditionListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['snyc_log'] = SyncLog.objects.last()
        return context
