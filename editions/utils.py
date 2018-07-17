import pandas as pd

from editions.models import Institution
from places.models import Place


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
