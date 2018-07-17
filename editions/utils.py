import pandas as pd

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from editions.models import Institution, Person, Period, Language, Edition
from places.models import Place
from handle.models import Pid


BOOLEAN_CHOICES = {
    "1": "yes",
    "0": "no",
    "no information provided": "no information provided",
    "not provided": "no information provided",
    "False": "no information provided",
    "not catalogued yet": "not catalogued yet",
    "trial": "no",
    "forthcoming": "no",
    "download book": "no",
    "N/A": "no",
    "0.5": "partially",
    "0,5": "partially",
    "PDF will be available": "no"
}


def create_institutions(df):
    """ creates institutions and their related places from a pandas.DataFrame """
    institutions = []
    for i, row in df.iterrows():
        inst = None
        if row['Institution Name']:
            inst, _ = Institution.objects.get_or_create(
                name=row['Institution Name']
            )
            if inst:
                if row['Institution GND']:
                    inst.gnd_id = row['Institution GND']

                if row['located at']:
                    place, _ = Place.objects.get_or_create(
                        name=row['located at'], place_type='city'
                    )
                    if row['part of']:
                        part_of, _ = Place.objects.get_or_create(
                            name=row['part of'], place_type='country'
                        )
                    place.part_of = part_of

                    if row['location geonames ID']:
                        try:
                            geonames = "http://www.geonames.org/{}".format(
                                int(row['location geonames ID'])
                            )
                        except ValueError:
                            geonames = None
                        if geonames:
                            place.geonames_id = geonames

                    if row['location Lat'] and row['location Lng']:
                        place.lat = row['location Lat']
                        place.lng = row['location Lng']
                    place.save()
                    inst.place = place

                if row['Institution Lat'] and row['Institution Lng']:
                    inst.lat = row['Institution Lat']
                    inst.lng = row['Institution Lng']

                if row['institution website']:
                    inst.website = row['institution website']

                inst.save()
                institutions.append(inst)
    return institutions


def create_editions(df):
    """ creates edition objects from specific pandas.DataFrame """
    eds_list = []
    ed_ct = ContentType.objects.get(app_label="editions", model="edition")
    for i, row in df.iterrows():
        bdate = None
        managers = None
        legacy_id = i+1
        ed, _ = Edition.objects.get_or_create(
            legacy_id=legacy_id
        )
        ed.name = row['Edition name']
        ed.url = row['URL']
        ed.scholarly = BOOLEAN_CHOICES[str(row['Scholarly'])]
        ed.digital = BOOLEAN_CHOICES[str(row['Digital'])]
        ed.edition = BOOLEAN_CHOICES[str(row['Edition'])]
        if row['Language']:
            ed.language.clear()
            for x in row['Language'].split(';'):
                lang, _ = Language.objects.get_or_create(
                            iso_code=(x.strip().lower())[:3]
                          )
                if lang:
                    ed.language.add(lang)
        ed.writing_support = row['Writing support']

        if row['Begin date']:
            try:
                bdate = pd.to_datetime(row['Begin date'])
            except ValueError:
                bdate = None
            if bdate:
                ed.begin_date = bdate
            ed.begin_date_comment = row['Begin date']

        if row['End date']:
            try:
                bdate = pd.to_datetime(row['End date'])
            except ValueError:
                bdate = None
            if bdate:
                ed.end_date = bdate
            ed.end_date_comment = row['End date']

        if row['Manager or Editor']:
            managers = [
                Person.objects.get_or_create(
                    name=pers.strip()
                )[0] for pers in row['Manager or Editor'].split(';')
            ]
            ed.manager.set(managers)

        if row['Institution(s)']:
            ed.institution.clear()
            for x in row['Institution(s)'].split(';'):
                try:
                    inst = Institution.objects.get(name=x.strip())
                except ObjectDoesNotExist:
                    inst = None
                if inst:
                    ed.institution.add(inst)

        ed.audience = str(row['Audience']).strip()
        ed.philological_statement = str(row['Philological statement']).strip()
        ed.textual_variance = str(row['Account of textual variance']).strip()
        ed.value_witnesses = str(row['Value of witnesses']).strip()
        ed.tei_transcription = str(row['XML-TEI Transcription']).strip()
        ed.download = str(row['XML(-TEI) available to download']).strip()
        ed.images = BOOLEAN_CHOICES[str(row['Images']).strip()]
        if row['Zoom images']:
            ed.zoom_images = BOOLEAN_CHOICES[str(row['Zoom images']).strip()]
        if row['Image manipulation (brightness, rotation, etc.)']:
            ed.image_manipulation = BOOLEAN_CHOICES[
                str(row['Image manipulation (brightness, rotation, etc.)']).strip()
            ]
        if row['Text-Image Linking']:
            ed.text_image = BOOLEAN_CHOICES[str(row['Text-Image Linking']).strip()]

        if row['Website language']:
            lang = None
            ed.website_language.clear()
            for x in row['Website language'].split(';'):
                lang, _ = Language.objects.get_or_create(
                            iso_code=(x.strip().lower())[:3]
                          )
                if lang:
                    ed.website_language.add(lang)

        if row['Glossary']:
            ed.glossary = BOOLEAN_CHOICES[str(row['Glossary']).strip()]
        if row['Indices']:
            ed.indices = BOOLEAN_CHOICES[str(row['Indices']).strip()]
        if row['String matching']:
            ed.search = BOOLEAN_CHOICES[str(row['String matching']).strip()]
        if row['Advanced search']:
            ed.advanced_search = BOOLEAN_CHOICES[str(row['Advanced search']).strip()]
        if row['Creative Commons License']:
            ed.cc_license = row['Creative Commons License'].strip()
        if row['Open source/Open access']:
            ed.open_source = row['Open source/Open access'].strip()
        if row['OCR or keyed?']:
            ed.key_or_ocr = row['OCR or keyed?'].strip()
        if row['Print-friendly view']:
            ed.print_friendly = BOOLEAN_CHOICES[str(row['Print-friendly view']).strip()]
        if row['Budget (rough)']:
            ed.budget = row['Budget (rough)'].strip()
        if row['Infrastructure']:
            ed.infrastructure = row['Infrastructure'].strip()
        if row['Current availability']:
            ed.current_availability = True
        else:
            current_availability = False
        if row['RIDE review']:
            ed.ride_review = row['RIDE review']
        if row['API']:
            ed.api = BOOLEAN_CHOICES[str(row['API']).strip()]

        if row['Repository of source material(s)']:
            ed.holding_repo.clear()
            for x in row['Repository of source material(s)'].split(';'):
                inst, _ = Institution.objects.get_or_create(name=x.strip())
                ed.holding_repo.add(inst)

        if row['Handle-PID']:
            pid = Pid.objects.get_or_create(
                handle=row['Handle-PID'],
                content_type=ed_ct,
                object_id=ed.legacy_id
            )
        else:
            pid = Pid.objects.get_or_create(
                content_type=ed_ct,
                object_id=ed.legacy_id
            )

        if row['Historical Period']:
            periods = [
                Period.objects.get_or_create(
                    name=pers.strip()
                )[0] for pers in row['Historical Period'].split(';')
            ]
            ed.historical_period.set(periods)

        ed.save()
        eds_list.append(ed)
    return eds_list
