import django_filters
from dal import autocomplete
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
        ("2", "Open Access and Open Source. All data underlying the digital edition is freely available for access, study, redistribution and improvement (reuse)."),
    )

BOOLEAN_CHOICES = (
        ("", "----"),
        ("yes", "yes"),
        ("no", "no"),
        ("no information provided", "no information provided"),
    )

CHOICES_PHILOLOGICAL = (
        ("", "----"),
        ("0", "No information on the editorial methods and practices nor on the source (digital or printed) of the text."),
        ("0.5", "No information on the source, but some information about the author, date and accuracy of the digital edition."),
        ("1", " Complete information on the source of the text, as well as on the author, date and accuracy of the digital edition. Digital Humanities standards implemented, including modelling, markup language, data structure and software. Values may include a large range of standards used, including HTML, XML-TEI etc."),
    )

CHOICES_TEXTUAL = (
        ("", "----"),
        ("0", "No account of textual variance is given. The digital edition is a reproduction of a given print edition without any account of variants."),
        ("0.5", "The digital edition is a reproduction of a given print scholarly edition and reproduces the selected textual variants extant in the apparatus criticus of that edition, or: the edition does not follow a digital paradigm, in that the variants are not automatically computable the way they are encoded."),
        ("1", "This edition is 'based on full-text transcription of original texts into electronic form'."),
    )

CHOICES_WITNESS = (
        ("", "----"),
        ("N/A", "Not applicable, as no information about the source of the text is given, though it is easily assumable that the source is another digital edition or a printed edition (possibly even a scholarly edition"),
        ("0", "The only witness modelled digitally is a printed non-scholarly edition, used as a source for the digital edition."),
        ("0.5", "Same as above, but the witness/source is a scholarly edition."),
        ("1", "The witnesses are traditional philological primary sources (including manuscripts, inscriptions or papyri)"),
    )
CHOICES_OCR = (
        ("", "----"),
        ("Keyed", "Keyed"),
        ("OCR", "OCR"),
    )


CHOICES_CC_License = (
    ("", "----"),
    ("no information provided", "no information provided"),
    ("0", "No CC License used."),
    ("0.5", " CC License but only for parts of the project."),
    ("1", "Everything under a CC License."),
)


class EditionListFilter(django_filters.FilterSet):
    name = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(
            url='editions-ac:edition-ac',
            attrs={
                'data-placeholder': 'Humbo...',
                'data-minimum-input-length': 3,
            },
        ),
        queryset=Edition.objects.all(),
        lookup_expr='icontains',
        label='Edition name',
        help_text=Edition._meta.get_field('name').help_text)
    url = django_filters.CharFilter(
        lookup_expr='icontains', help_text=Edition._meta.get_field('url').help_text)
    institution__name = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(
            url='editions-ac:institution-ac',
            attrs={
                'data-placeholder': 'Bologna...',
                'data-minimum-input-length': 3,
            },
        ),
        queryset=Institution.objects.all(),
        lookup_expr='icontains',
        label='Institution',
        help_text=Edition._meta.get_field('institution').help_text
    )
    historical_period = django_filters.ModelMultipleChoiceFilter(
        queryset=Period.objects.all(), label='Period',
        help_text=Edition._meta.get_field('historical_period').help_text)
    scholarly = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, help_text=Edition._meta.get_field('scholarly').help_text)
    digital = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, help_text=Edition._meta.get_field('digital').help_text)
    edition = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, help_text=Edition._meta.get_field('edition').help_text)
    # prototype = django_filters.ChoiceFilter(
    #     choices=BOOLEAN_CHOICES, help_text=Edition._meta.get_field('prototype').help_text)
    language = django_filters.ModelMultipleChoiceFilter(
        queryset=Language.objects.all(), help_text=Edition._meta.get_field('language').help_text)
    writing_support = django_filters.CharFilter(
        lookup_expr='icontains', help_text=Edition._meta.get_field('writing_support').help_text)
    begin_date = django_filters.DateFilter(
        help_text=Edition._meta.get_field('begin_date').help_text)
    end_date = django_filters.DateFilter(
        help_text=Edition._meta.get_field('end_date').help_text)
    manager__name = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(
            url='editions-ac:person-ac',
            attrs={
                'data-placeholder': 'e.g. Dániel Kiss',
                'data-minimum-input-length': 3,
            },
        ),
        queryset=Person.objects.all(),
        lookup_expr='icontains',
        label='Manager',
        help_text=Edition._meta.get_field('manager').help_text
    )
    audience = django_filters.CharFilter(
        lookup_expr='icontains', help_text=Edition._meta.get_field('audience').help_text)
    philological_statement = django_filters.ChoiceFilter(
        choices=CHOICES_PHILOLOGICAL, help_text=Edition._meta.get_field('philological_statement').help_text)
    textual_variance = django_filters.ChoiceFilter(
        choices=CHOICES_TEXTUAL, help_text=Edition._meta.get_field('textual_variance').help_text)
    value_witnesses = django_filters.ChoiceFilter(
        choices=CHOICES_WITNESS, help_text=Edition._meta.get_field('value_witnesses').help_text)
    tei_transcription = django_filters.ChoiceFilter(
        choices=CHOICES_TEI, label='XML-TEI transcription',
        help_text=Edition._meta.get_field('tei_transcription').help_text)
    download = django_filters.ChoiceFilter(
        choices=CHOICES_DOWNLOAD, label='XML-TEI transcription to download',
        help_text=Edition._meta.get_field('download').help_text)
    images = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('images').help_text)
    zoom_images = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('zoom_images').help_text)
    image_manipulation = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('image_manipulation').help_text)
    text_image = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('text_image').help_text)
    source_translation = django_filters.CharFilter(
        lookup_expr='icontains', label='Source text translation',
        help_text=Edition._meta.get_field('source_translation').help_text)
    website_language = django_filters.ModelMultipleChoiceFilter(
        queryset=Language.objects.all(), help_text=Edition._meta.get_field('website_language').help_text)
    glossary = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('glossary').help_text)
    indices = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('indices').help_text)
    search = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, label='String matching search',
        help_text=Edition._meta.get_field('search').help_text)
    advanced_search = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('advanced_search').help_text)
    cc_license = django_filters.ChoiceFilter(
        choices=CHOICES_CC_License, label='Creative Commons License',
        help_text=Edition._meta.get_field('cc_license').help_text)
    open_source = django_filters.ChoiceFilter(
        choices=CHOICES_OPENSOURCE, label='Open Access/Source',
        help_text=Edition._meta.get_field('open_source').help_text)
    infrastructure = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Edition._meta.get_field('infrastructure').help_text)
    key_or_ocr = django_filters.ChoiceFilter(
        choices=CHOICES_OCR, label='OCR or keyed?',
        help_text=Edition._meta.get_field('key_or_ocr').help_text)
    print_friendly = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('print_friendly').help_text)
    api = django_filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES,
        help_text=Edition._meta.get_field('api').help_text)
    ride_review = django_filters.BooleanFilter(
        lookup_expr='isnull', help_text="Is there a RIDE review ?",
        exclude=True, label="RIDE review"
        )

    def country_name_filter(self, queryset, value):
        return queryset.filter(institution__place__part_of__name__icontains=value).distinct()

    def city_name_filter(self, queryset, value):
        return queryset.filter(institution__place__name__icontains=value).distinct()

    class Meta:
        model = Edition
        fields = ['name', 'institution__name', 'manager__name']
