from django.db import models
from django.contrib.auth.models import User

from places.models import Place


class SyncLog(models.Model):
    actor = models.ForeignKey(User, blank=True)
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


class Institution(models.Model):
    name = models.CharField(
        max_length=255, blank=True, help_text="The Instituion's name."
    )
    place = models.ForeignKey(
        Place, blank=True, null=True, help_text="Place which the institution is associated with."
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

    def __str__(self):
        return "{}".format(self.name)


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

    BOOLEAN_CHOICES = (
        ("", "----"),
        ("yes", "yes"),
        ("no", "no"),
        ("no information provided", "no information provided"),
    )
    name = models.CharField(
        max_length=255, blank=True, help_text="The name of the edition (project).")
    url = models.CharField(
        max_length=255, blank=True, help_text="The URL of the edition (project).")
    historical_period = models.ManyToManyField(
        Period, blank=True, help_text="This field broadly categorises an edition by periods"
    )
    scholarly = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="An edition must be critical, must have critical components - a pure facsimile is not an edition, a digital library is not an edition. (Patrick Sahle)"
    )
    digital = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="A digital edition can not be converted to a printed edition without substantial loss of content or functionality - vice versa: a retrodigitized printed edition is not a Scholarly Digital Edition (but it may evolve into a Scholarly Digital Edition through new content or functionalities). (Patrick Sahle)"
    )
    edition = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="An edition must represent its material (usually as transcribed/edited text) - a catalog, an index, a descriptive database is not an edition. (Patrick Sahle)"
    )
    # prototype = models.CharField(
    #     choices=BOOLEAN_CHOICES, blank=True, max_length=40,
    #     help_text="A Scholarly Digital Edition (SDE) is a publication of the material in question; a SDE project is not the same as a SDE, that means a SDE is more than a plan or a prototype. (Patrick Sahle)"
    # )
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
    end_date = models.DateField(
        null=True, blank=True,
        help_text="Year the project ended. If ongoing, leave blank."
    )
    manager = models.ManyToManyField(
        Person, blank=True, help_text="Name of project manager(s)."
    )
    institution = models.ManyToManyField(
        Institution, blank=True,
        help_text="Name(s) of institution(s) involved in the project."
    )
    audience = models.TextField(
        blank=True,
        help_text="The target audience of the edition project (scholars, general public, etc.)."
    )
    CHOICES_PHILOLOGICAL = (
        ("", "----"),
        ("0", "No information on the editorial methods and practices nor on the source (digital or printed) of the text."),
        ("0.5", "No information on the source, but some information about the author, date and accuracy of the digital edition."),
        ("1", " Complete information on the source of the text, as well as on the author, date and accuracy of the digital edition. Digital Humanities standards implemented, including modelling, markup language, data structure and software. Values may include a large range of standards used, including HTML, XML-TEI etc."),
    )
    philological_statement = models.CharField(
        blank=True, max_length=255,
        choices=CHOICES_PHILOLOGICAL
    )
    CHOICES_TEXTUAL = (
        ("", "----"),
        ("0", "No account of textual variance is given. The digital edition is a reproduction of a given print edition without any account of variants."),
        ("0.5", "The digital edition is a reproduction of a given print scholarly edition and reproduces the selected textual variants extant in the apparatus criticus of that edition, or: the edition does not follow a digital paradigm, in that the variants are not automatically computable the way they are encoded."),
        ("1", "This edition is 'based on full-text transcription of original texts into electronic form'."),
    )
    textual_variance = models.CharField(
        blank=True, max_length=255,
        choices=CHOICES_TEXTUAL,
        verbose_name="Account of textual variance"
    )
    CHOICES_WITNESS = (
        ("", "----"),
        ("N/A", "Not applicable, as no information about the source of the text is given, though it is easily assumable that the source is another digital edition or a printed edition (possibly even a scholarly edition"),
        ("0", "The only witness modelled digitally is a printed non-scholarly edition, used as a source for the digital edition."),
        ("0.5", "Same as above, but the witness/source is a scholarly edition."),
        ("1", "The witnesses are traditional philological primary sources (including manuscripts, inscriptions or papyri)"),
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
        help_text="The values 1 or 0 are used to tell us if the edition comes with images."
    )
    zoom_images = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to tell us if the user can zoom in or out of images within the edition."
    )
    image_manipulation = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 and 0 are used to tell us whether the user can manipulate these images in any way within the edition (brightness, saturation, etc.)."
    )
    text_image = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The transcription and the image are linked so that clicking on a word in the image brings up the corresponding textual token and viceversa.",
        verbose_name="Text-image linking"
    )
    source_translation = models.CharField(
        blank=True, max_length=3,
        help_text="The project provides a translation of the source text. If so, the corresponding three-letter ISO code should be used. If not, type 0.",
        verbose_name="Source text translation"
    )
    website_language = models.ManyToManyField(
        Language, blank=True, max_length=3, related_name="lang_website",
        help_text="The language the project website is written in. Three-letter ISO Codes should be used."
    )
    glossary = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to tell us if the edition provides a glossary."
    )
    indices = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to tell us if the edition provides indices."
    )
    search = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text = "The values 1 or 0 are used to tell us if the edition provides string matching search possibilities.",
        verbose_name="String matching search"
    )
    advanced_search = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to tell us if the edition provides an advanced search functionality."
    )
    cc_license = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to specify if the project is protected by a Creative Commons License.",
        verbose_name="Creative Commons License"
    )
    CHOICES_OPENSOURCE = (
        ("", "----"),
        ("no information provided", "no information provided"),
        ("0", "Proprietary, all material is copyrighted. The ‘source’ is closed and not reusable by other research projects. To access the material, users must pay a subscription."),
        ("0.5", "Same as above, but the subscription is free of charge."),
        ("1", "Open Access. The texts may be accessed through specific software, but the source is not accessible."),
        ("1.5", " Open Access and Open Source. All data underlying the digital edition is freely available for access, study, redistribution and improvement (reuse)"),
    )
    open_source = models.CharField(
        blank=True, max_length=255,
        choices=CHOICES_OPENSOURCE,
        verbose_name="Open Source/Open Access", help_text='add helptext'
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
        blank=True, max_length=12,
        help_text="The source text was digitised with Optical Character Recognition (OCR) software or manually keyed in.",
        choices=CHOICES_OCR,
        verbose_name="OCR or keyed?"
    )
    print_friendly = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to tell if the project provides a print-friendly view of the text (e.g. PDF)."
    )
    api = models.CharField(
        choices=BOOLEAN_CHOICES, blank=True, max_length=40,
        help_text="The values 1 or 0 are used to specify if the project comes with an API (Application Programming Interface)."
    )

    def __str__(self):
        return "{}".format(self.name)
