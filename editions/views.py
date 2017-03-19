import csv
import re
import time
import datetime
import requests
from django.http import HttpResponse
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from .models import *
from places import *
from .forms import EditionForm


def institution_csv(request):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    response = HttpResponse(content_type='text/csv')
    filename = "institutions_{}.csv".format(timestamp)
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
    writer = csv.writer(response, delimiter=";")
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
    template_name = "editions/institution_csv.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return Institution.objects.all()


@login_required
def sync(request):
    context = RequestContext(request)
    return render(request, 'editions/sync.html', context)


@login_required
def sync_status(request):
    try:
        userobject = request.user
    except:
        userobject = None
    context = {}
    context["nr_editions_start"] = len(Edition.objects.all())
    url = 'https://raw.githubusercontent.com/gfranzini/digEds_cat/master/digEds_cat.csv'
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        datalist = list(cr)
        cleaned_data = []
    for row in datalist:
        cleaned_row = []
        for cell in row:
            if str(cell) == "":
                cell = re.sub("", "no information provided", cell)
                cleaned_row.append(cell)
            else:
                cleaned_row.append(cell)
        cleaned_data.append(cleaned_row)
    BOOLEAN_CHOICES = {
        "1": "yes",
        "0": "no",
        "no information provided": "no information provided",
        "trial": "no",
        "forthcoming": "no",
        "download book": "no",
        "N/A": "no",
        "0.5": "no",
        "0,5": "no",
        "PDF will be available": "no"}
    counter = 1
    for row in cleaned_data[1:-1]:
        if row[3] != "":
            temp_per, _ = Period.objects.get_or_create(name=row[0])
            temp_ed, _ = Edition.objects.get_or_create(legacy_id=counter)
            temp_ed.url = row[3]
            temp_ed.name = row[2]
            temp_ed.scholarly = BOOLEAN_CHOICES[str(row[4])]
            temp_ed.digital = BOOLEAN_CHOICES[str(row[5])]
            temp_ed.edition = BOOLEAN_CHOICES[str(row[6])]
            if row[7] != "":
                langs1 = row[7].split(",")
                for x in langs1:
                    temp_lang_source, _ = Language.objects.get_or_create(
                        iso_code=(x.strip().lower())[:3])
                    temp_ed.language.add(temp_lang_source)
            temp_ed.writing_support = row[8]
            if row[9] != "":
                start_date = re.match("\d{4}", row[9])
                if start_date:
                    start_date = datetime.datetime.strptime(start_date.group(), '%Y')
                    temp_ed.begin_date = start_date
            if row[10] != "":
                end_date = re.match("\d{4}", row[10])
                if end_date:
                    end_date = datetime.datetime.strptime(end_date.group(), '%Y')
                    temp_ed.end_date = end_date
            for pers in row[11].split(";"):
                pers_temp, _ = Person.objects.get_or_create(name=pers.strip())
                temp_ed.manager.add(pers_temp)
            for inst in row[12].split(";"):

                try:
                    inst_temp = Institution.objects.get(name=inst.strip())
                    temp_ed.institution.add(inst_temp)
                except:
                    pass
            temp_ed.audience = str(row[13])
            temp_ed.philological_statement = str(row[14])
            temp_ed.textual_variance = str(row[15])
            temp_ed.value_witnesses = str(row[16])
            temp_ed.tei_transcription = str(row[17]).strip()
            temp_ed.download = str(row[18]).strip()
            temp_ed.images = BOOLEAN_CHOICES[str(row[19])]
            temp_ed.zoom_images = BOOLEAN_CHOICES[str(row[20])]
            temp_ed.image_manipulation = BOOLEAN_CHOICES[str(row[21])]
            temp_ed.text_image = BOOLEAN_CHOICES[str(row[22])]
            if row[24] != "":
                langs = row[24].split(";")
                for y in langs:
                    temp_lang_website, _ = Language.objects.get_or_create(
                        iso_code=(y.strip().lower())[:3])
                    temp_ed.website_language.add(temp_lang_website)
            temp_ed.glossary = BOOLEAN_CHOICES[str(row[25])]
            temp_ed.indices = BOOLEAN_CHOICES[str(row[26])]
            temp_ed.search = BOOLEAN_CHOICES[str(row[27])]
            temp_ed.advanced_search = BOOLEAN_CHOICES[str(row[28])]
            temp_ed.cc_license = row[29]
            temp_ed.open_source = row[30]
            temp_ed.key_or_ocr = str(row[37])
            temp_ed.print_friendly = BOOLEAN_CHOICES[str(row[39])]
            temp_ed.infrastructure = str(row[45])
            try:
                alive = int(row[46])
                temp_ed.current_availability = alive
            except:
                pass
            temp_ed.historical_period.add(temp_per)
            temp_ed.api = BOOLEAN_CHOICES[str(row[32])]
            temp_ed.save()
            counter += 1
    context["nr_editions_now"] = len(Edition.objects.all())
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
