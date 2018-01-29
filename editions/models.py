import json
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from places.models import Place


class SyncLog(models.Model):
    actor = models.ForeignKey(User, blank=True, on_delete=models.PROTECT)
    sync_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "last time synced {} by {}".format(
            (self.sync_date).strftime('%Y/%m/%d %H:%M:%S'), self.actor
        )


class Person(models.Model):
    name = models.CharField(
        max_length=255, blank=True, help_text="The Person's name."
    )

    def __str__(self):
        return "{}".format(self.name)

    def get_browsing_url(self):
        return "{}?manager__name={}".format(
            reverse('browsing:browse_editions'),
            self.pk
        )


class Institution(models.Model):
    name = models.CharField(
        max_length=255, blank=True, help_text="The Instituion's name."
    )
    place = models.ForeignKey(
        Place, blank=True, null=True,
        help_text="Place with which the institution is associated with.",
        on_delete=models.PROTECT
    )
    gnd_id = models.CharField(
        max_length=255, blank=True, help_text="GND id of Institution."
    )
    lat = models.DecimalField(
        max_digits=20, decimal_places=12,
        blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=20, decimal_places=12, blank=True, null=True
    )
    website = models.CharField(
        max_length=255, blank=True, help_text="Website of the Institution."
    )

    def __str__(self):
        return "{}".format(self.name)

    def get_browsing_url(self):
        return "{}?institution__name={}".format(
            reverse('browsing:browse_editions'),
            self.pk
        )


class Period(models.Model):
    name = models.CharField(
        max_length=255, blank=True, help_text="The Periods Name."
    )
    start_date = models.IntegerField(blank=True, null=True)
    end_date = models.IntegerField(blank=True, null=True)
    periodO_id = models.CharField(
        max_length=255, blank=True, help_text="http://perio.do/"
    )

    def __str__(self):
        return "{}".format(self.name)


class Language(models.Model):
    iso_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.iso_code)


class Edition(models.Model):
    """Holds the (meta)data of a digital editions project. Information taken from
    https://github.com/gfranzini/digEds_cat/wiki/Contribute"""

    NULL_BOOLEAN_CHOICES = (
        (None, "unknown"),
        (True, "yes"),
        (False, "no")
    )

    BOOLEAN_CHOICES = (
        ("", "----"),
        ("yes", "yes"),
        ("no", "no"),
        ("no information provided", "no information provided"),
    )
    legacy_id = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=255, blank=True, verbose_name="Name of the Project",
        help_text="The name of the project."
    )
    url = models.CharField(
        max_length=255, blank=True, help_text="The URL of the project.")
    historical_period = models.ManyToManyField(
        Period, blank=True, help_text="Historical period to which the source text belongs."
    )
    scholarly = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="An edition must be critical, must have critical components - a pure facsimile\
        is not an edition, a digital library is not an edition (Patrick Sahle)."
    )
    digital = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="A digital edition can not be converted to a printed edition without substantial\
        loss of content or functionality - vice versa: a retrodigitized printed edition is not a\
        Scholarly Digital Edition (but it may evolve into a Scholarly Digital Edition through new\
        content or functionalities) (Patrick Sahle)."
    )
    edition = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="An edition must represent its material (usually as transcribed/edited text)\
        - a catalog, an index, a descriptive database is not an edition (Patrick Sahle)."
    )
    language = models.ManyToManyField(
        Language, blank=True, related_name="lang_source",
        help_text="The language(s) of the source text. Three-letter ISO Codes are used."
    )
    writing_support = models.CharField(
        max_length=255, blank=True,
        help_text="The nature of the source text (manuscript, letter, notebook, etc.)."
    )
    begin_date = models.DateField(
        null=True, blank=True,
        help_text="Year the project started."
    )
    begin_date_comment = models.CharField(
        max_length=50, blank=True
    )
    end_date = models.DateField(
        null=True, blank=True,
        help_text="Year the project ended. If ongoing, leave blank."
    )
    end_date_comment = models.CharField(
        max_length=50, blank=True
    )
    manager = models.ManyToManyField(
        Person, blank=True, help_text="Name of project manager(s)."
    )
    institution = models.ManyToManyField(
        Institution, blank=True,
        help_text="Name(s) of institution(s) involved in the project.", related_name="projects"
    )
    audience = models.TextField(
        blank=True,
        help_text="The target audience of the project (scholars, general public, etc.)."
    )
    CHOICES_PHILOLOGICAL = (
        ("", "----"),
        ("0", "No information on the editorial methods and practices nor on the source\
        (digital or printed) of the text."),
        ("0.5", "No information on the source, but some information about the author,\
        date and accuracy of the digital edition."),
        ("1", " Complete information on the source of the text, as well as on the author,\
        date and accuracy of the digital edition. Digital Humanities standards implemented,\
        including modelling, markup language, data structure and software."),
    )
    philological_statement = models.CharField(
        blank=True, max_length=255,
        choices=CHOICES_PHILOLOGICAL
    )
    CHOICES_TEXTUAL = (
        ("", "----"),
        ("0", "No account of textual variance is given. The digital edition is a reproduction\
        of a given print edition without any account of variants."),
        ("0.5", "The digital edition is a reproduction of a given print scholarly edition and\
        reproduces the selected textual variants extant in the apparatus criticus of that edition,\
        or: the edition does not follow a digital paradigm, in that the variants are\
        not automatically computable the way they are encoded."),
        ("1", "This edition is based on full-text transcription of original texts\
        into electronic form."),
    )
    textual_variance = models.CharField(
        blank=True, max_length=255,
        choices=CHOICES_TEXTUAL,
        verbose_name="Account of textual variance"
    )
    CHOICES_WITNESS = (
        ("", "----"),
        ("N/A", "Not applicable, as no information about the source of the text is given,\
        though it is easily assumable that the source is another digital edition\
        or a printed edition (possibly even a scholarly edition"),
        ("0", "The only witness modelled digitally is a printed non-scholarly edition,\
        used as a source for the digital edition."),
        ("0.5", "Same as above, but the witness/source is a scholarly edition."),
        ("1", "The witnesses are traditional philological primary sources."),
    )
    value_witnesses = models.CharField(
        choices=CHOICES_WITNESS, blank=True, null=True, max_length=255,
        verbose_name="Value of witnesses"
    )
    CHOICES_TEI = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "XML not used"),
        ("0.5", "XML but not TEI"),
        ("1", "XML-TEI is used"),
    )
    tei_transcription = models.CharField(
        choices=CHOICES_TEI, blank=True, null=True, max_length=255,
        help_text="The source text is encoded in XML-TEI.",
        verbose_name="XML-TEI transcription"
    )
    CHOICES_DOWNLOAD = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "no"),
        ("0.5", "partially"),
        ("1", "yes"),
    )
    download = models.CharField(
        choices=CHOICES_DOWNLOAD, blank=True, null=True, max_length=255,
        help_text="The XML-TEI encoded text is available for download.",
        verbose_name="XML-TEI transcription to download"
    )
    images = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project comes with images."
    )
    zoom_images = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The images are zoomable."
    )
    image_manipulation = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The images can be manipulated in some way within\
        the edition (brightness, rotation, etc.)."
    )
    text_image = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The transcription and the image are linked so that clicking on a word\
        in the image brings up the corresponding textual token and viceversa.",
        verbose_name="Text-image linking"
    )
    source_translation = models.CharField(
        blank=True, max_length=3,
        help_text="The project provides a translation of the source text.",
        verbose_name="Source text translation"
    )
    website_language = models.ManyToManyField(
        Language, blank=True, max_length=3, related_name="lang_website",
        help_text="The language of the website/interface."
    )
    glossary = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project provides a glossary."
    )
    indices = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project provides indices."
    )
    search = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project provides string matching search possibilities.",
        verbose_name="String matching search"
    )
    advanced_search = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project provides an advanced search functionality."
    )
    CHOICES_CC_License = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "no"),
        ("0.5", "partial"),
        ("1", "yes"),
    )
    cc_license = models.CharField(
        choices=CHOICES_CC_License, blank=True, max_length=40,
        help_text="The project is protected by a Creative Commons License.",
        verbose_name="Creative Commons License"
    )
    CHOICES_OPENSOURCE = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "Proprietary, all material is copyrighted. The ‘source’ is closed and not reusable \
         by other research projects. To access the material, users must pay a subscription."),
        ("0.5", "Same as above, but the subscription is free of charge."),
        ("1", "Open Access. The texts may be accessed through specific software,\
        but the source is not accessible."),
        ("1.5", "Open Access and Open Source. Part of the data underlying the digital edition\
        (e.g. text but not images) is freely available for access and reuse."),
        ("2", "Open Access and Open Source. All data underlying the digital edition \
        is freely available for access and reuse.")
    )
    open_source = models.CharField(
        blank=True, max_length=255,
        choices=CHOICES_OPENSOURCE,
        verbose_name="Open Source/Open Access",
        help_text='The project adheres to an Open Source/Access policy.'
    )
    infrastructure = models.CharField(
        blank=True, max_length=255,
        help_text="The technologies used to run the project (Drupal, Omeka, MySQL, etc.)."
    )
    CHOICES_OCR = (
        ("", "----"),
        ("Keyed", "Keyed"),
        ("OCR", "OCR"),
    )
    key_or_ocr = models.CharField(
        blank=True, max_length=40,
        help_text="The source text was digitised with Optical Character Recognition (OCR) software\
        or manually keyed in.",
        choices=CHOICES_OCR,
        verbose_name="OCR or keyed?"
    )
    print_friendly = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project provides a print-friendly view of the text (e.g. PDF)."
    )
    api = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The project comes with an API (Application Programming Interface)."
    )
    current_availability = models.NullBooleanField(
        blank=True, null=True, help_text="1 means STILL AVAILABLE and 0 means DEAD.")
    ride_review = models.CharField(
        blank=True, null=True, help_text="The project has been reviewed in the RIDE Journal.",
        max_length=500
    )
    budget = models.CharField(
        blank=True, max_length=250, help_text="How much the project cost."
    )
    holding_repo = models.ManyToManyField(
        Institution, blank=True, verbose_name="Repository of Source Material(s)",
        help_text="The institution(s) that house the source text(s).", related_name="holding_repo"
    )
    sahle_cat = models.NullBooleanField(
        choices=NULL_BOOLEAN_CHOICES,
        blank=True, null=True, verbose_name="Sahle Catalog",
        help_text="Indicates whether a digital edition is also present in Patrick Sahle's\
        Catalog of Digital Scholarly Editions (http://www.digitale-edition.de/).\
        The values 0 [no] or 1 [yes] are used."
    )

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('editions:edition_detail', kwargs={'pk': self.legacy_id})

    def netviz_data(self, json_out=True):
        nodes = [
            {
                'id': "edition_{}".format(self.pk),
                'title': "{}".format(self.name),
                'color': "red",
                'type': "Edition",
                'url': self.get_absolute_url()
            }
        ]
        edges = []

        for y in self.institution.all():
            node = {
                'id': "institution_{}".format(y.pk),
                'title': y.name,
                'color': 'green',
                'type': 'Institution',
                'url': y.get_browsing_url()
            }
            edge = {
                'from': "edition_{}".format(self.pk),
                'to': "institution_{}".format(y.pk)
            }
            if node not in nodes:
                nodes.append(node)
            edges.append(edge)
            try:
                newedge = {
                    'from': "institution_{}".format(y.pk),
                    'to': "place_{}".format(y.place.pk)
                }
                newnode = {
                    'id': "place_{}".format(y.place.pk),
                    'title': "{}".format(y.place.name),
                    'color': "yellow",
                    'type': "Place",
                }
                if newnode not in nodes:
                    nodes.append(newnode)
                edges.append(newedge)
            except AttributeError:
                pass
        for y in self.manager.all():
            node = {
                'id': "person_{}".format(y.pk),
                'title': y.name,
                'color': "blue",
                'url': y.get_browsing_url()
            }
            nodes.append(node)
            edge = {
                'from': "edition_{}".format(self.pk),
                'to': "person_{}".format(y.pk)
            }
            edges.append(edge)
        data = {
                'nodes': nodes,
                'edges': edges
            }
        if json_out:
            return json.dumps(data)
        else:
            return data
