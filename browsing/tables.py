import django_tables2 as tables
from django_tables2.utils import A
from editions.models import *
from places.models import *


class EditionTable(tables.Table):
    legacy_id = tables.Column(verbose_name='ID')
    name = tables.LinkColumn('editions:edition_detail', args=[A('legacy_id')], verbose_name='edition name')
    institution = tables.Column(empty_values=())

    def render_institution(self, record):   # for ManyToMany field to display all institutions
        if record.institution.all():
            return ', '.join([institution.name for institution in record.institution.all()])
        return '-'

    class Meta:
        model = Edition
        fields = ['legacy_id', 'name', 'institution']
        attrs = {"class": "table table-hover table-responsive table-striped"}



# class InstitutionTable(tables.Table):
#     name = tables.Column(verbose_name='place name')
#     alternative_name = tables.Column(accessor='alternative_name.name')
#     geonames_id = tables.Column(verbose_name='geonames id')

#     class Meta:
#         model = Place
#         fields = ['name', 'alternative_name.name', 'geonames_id']
#         attrs = {"class": "table table-hover table-striped table-condensed"}
