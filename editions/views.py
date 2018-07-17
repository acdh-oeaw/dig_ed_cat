import csv
import re
import time
import datetime
import requests
import itertools
import json
import pandas as pd
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import *
from places import *
from .forms import EditionForm
from browsing.filters import EditionListFilter
from editions.utils import BOOLEAN_CHOICES, create_institutions, create_editions


def institution_csv(request):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    response = HttpResponse(content_type='text/csv')
    filename = "institutions_{}".format(timestamp)
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
    writer = csv.writer(response, delimiter=",")
    writer.writerow([
        'Institution Name', 'Institution GND',
        'Institution Lat', 'Institution Lng',
        'located at', 'location geonames ID', 'location Lat',
        'location Lng', 'part of', 'type of location']
    )
    for x in Institution.objects.all():
        if x.place:
            writer.writerow(
                [x.name, x.gnd_id, x.lat, x.lng, x.place.name, x.place.geonames_id,
                    x.place.lat, x.place.lng, x.place.part_of, x.place.place_type]
            )
        else:
            writer.writerow([x.name, x.gnd_id, x.lat, x.lng])
    return response


class InstitutionListView(generic.ListView):
    template_name = "editions/institution_list.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return Institution.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionListView, self).dispatch(*args, **kwargs)


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'editions/institution_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(**kwargs)
        return context


@login_required
def sync(request):
    context = {}
    return render(request, 'editions/sync.html', context)


@login_required
def sync_status(request):
    try:
        userobject = request.user
    except AttributeError:
        userobject = None
    context = {}
    context["nr_editions_start"] = Edition.objects.count()
    base_url = "https://raw.githubusercontent.com/gfranzini/digEds_cat/"

    place_url = '{}master/institutions_places_enriched.csv'.format(base_url)
    df = pd.read_csv(place_url).fillna(False)
    create_institutions(df)
    df = None

    ed_url = 'https://raw.githubusercontent.com/gfranzini/digEds_cat/master/digEds_cat.csv'
    df = pd.read_csv(ed_url).fillna(False)[:-1]
    create_editions(df)

    context["nr_editions_now"] = Edition.objects.count()
    new_log = SyncLog(actor=userobject)
    new_log.save()
    context['log'] = new_log
    return render(request, 'editions/sync_status.html', context)


class EditionListView(generic.ListView):
    template_name = "editions/list_editions.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return Edition.objects.all()


class EditionDetailView(DetailView):
    model = Edition
    template_name = "editions/edition_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EditionDetailView, self).get_context_data(**kwargs)
        edition_ids = [x.legacy_id for x in Edition.objects.all()]
        self_id = int(self.kwargs['pk'])
        if self_id == edition_ids[-1]:
            next_entry = None
        else:
            next_entry = edition_ids[edition_ids.index(self_id) + 1]
        context["next_entry"] = next_entry

        if edition_ids.index(self_id) == 0:
            previous_entry = None
        else:
            previous_entry = edition_ids[edition_ids.index(self_id) - 1]
        context["previous_entry"] = previous_entry
        # netvis context
        instance = Edition.objects.get(legacy_id=self_id)
        net_data = instance.netviz_data(json_out=True, show_labels=True)
        context['netviz_data'] = net_data
        return context


@login_required
def edit_edition(request, pk):
    instance = get_object_or_404(Edition, legacy_id=pk)
    if request.method == "POST":
        form = EditionForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('editions:edition_detail', pk=pk)
        else:
            return render(request, 'editions/edit_edition.html', {'form': form})
    else:
        form = EditionForm(instance=instance)
        return render(request, 'editions/edit_edition.html', {'form': form})
