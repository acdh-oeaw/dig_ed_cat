from django.db import models


class AlternativeName(models.Model):
    name = models.CharField(max_length=250, blank=True, help_text="Alternative Name")

    def __str__(self):
        return self.name


class Place(models.Model):

    """Holds information about places."""
    name = models.CharField(
        max_length=250, blank=True, help_text="Normalized name"
    )
    alternative_name = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names"
    )
    geonames_id = models.CharField(
        max_length=50, blank=True,
        help_text="GND-ID"
    )
    lat = models.DecimalField(
        max_digits=20, decimal_places=12,
        blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=20, decimal_places=12, blank=True, null=True
    )
    part_of = models.ForeignKey(
        "Place", null=True, blank=True, help_text="A place (country) this place is part of."
    )

    def __str__(self):
        if self.alternative_name.exists():
            return self.name+" (" + " ".join([str(x.name) for x in self.alternative_name.all()]) + ")"
        else:
            return self.name
