import django_filters
from editions.models import *
from places.models import *

django_filters.filters.LOOKUP_TYPES = [
	('', '---------'),
	('exact', 'Is equal to'),
	('iexact', 'Is equal to (case insensitive)'),
	('not_exact', 'Is not equal to'),
	('lt', 'Lesser than/before'),
	('gt', 'Greater than/after'),
	('gte', 'Greater than or equal to'),
	('lte', 'Lesser than or equal to'),
	('startswith', 'Starts with'),
	('endswith', 'Ends with'),
	('contains', 'Contains'),
	('icontains', 'Contains (case insensitive)'),
	('not_contains', 'Does not contain'),
]

CHOICES_TEI = (
		("", "----"),
		("no information provided", "no information provided"),
		("0", "XML not used"),
		("0.5", "XML but not TEI"),
		("1", "XML-TEI is used"),
	)

CHOICES_DOWNLOAD = (
		("", "----"),
		("no information provided", "no information provided"),
		("0", "no"),
		("0.5", "partially"),
		("1", "yes"),
	)

CHOICES_OPENSOURCE = (
		("", "----"),
		("No information provided.", "no information provided"),
		("0", "Proprietary, all material is copyrighted. The ‘source’ is closed and not reusable by other research projects. To access the material, users must pay a subscription."),
		("0.5", "Same as above, but the subscription is free of charge."),
		("1", "Open Access. The texts may be accessed through specific software, but the source is not accessible."),
		("1.5", " Open Access and Open Source. All data underlying the digital edition is freely available for access, study, redistribution and improvement (reuse)"),
	)

BOOLEAN_CHOICES = (
 		("", "----"),
        ("yes", "yes"),
        ("no", "no"),
        ("no information provided", "no information provided"),
    )

class EditionListFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(
		lookup_expr='icontains', label='Edition name', help_text=Edition._meta.get_field('name').help_text
		)
	url = django_filters.CharFilter(
		lookup_expr='icontains', help_text=False
		)
	institution__name = django_filters.ModelMultipleChoiceFilter(
		queryset=Institution.objects.all(), help_text=False
		)
	historical_period__name = django_filters.ModelMultipleChoiceFilter(
		queryset=Period.objects.all(),label='Period',help_text=False
		)
	manager__name = django_filters.ModelMultipleChoiceFilter(
		queryset=Person.objects.all(), help_text=False
		)
	tei_transcription = django_filters.ChoiceFilter(
		choices=CHOICES_TEI, label='XML-TEI transcription',help_text=False
		)
	download = django_filters.ChoiceFilter(
		choices=CHOICES_DOWNLOAD, label='XML-TEI transcription to download',help_text=False
		)
	scholarly = django_filters.ChoiceFilter(
		choices=BOOLEAN_CHOICES, label='scholarly', help_text=False
		)
	open_source = django_filters.ChoiceFilter(
		choices=CHOICES_OPENSOURCE, label='Open Access/Source',
		help_text=Edition._meta.get_field('open_source').help_text
		)

	class Meta:
		model = Edition
		fields = ['name']


# class InstitutionListFilter(django_filters.FilterSet): #refers to places models
# 	name = django_filters.CharFilter(lookup_expr='icontains', label='Place name', help_text=False)
# 	alternative_name__name = django_filters.ModelMultipleChoiceFilter(queryset=AlternativeName.objects.all(), help_text=False)
# 	geonames_id = django_filters.CharFilter(lookup_expr='icontains', label='Geonames ID', help_text=False)

# 	class Meta:
# 		model = Place
# 		fields = ['name']
