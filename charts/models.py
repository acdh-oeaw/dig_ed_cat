from django.db import models


class ChartType(models.Model):

    """Describes possible chart types"""

    name = models.CharField(
        max_length=255, blank=True, help_text="A name of the chart type."
    )
    icon = models.CharField(
        max_length=255, blank=True,
        help_text="A HTML snippet which could be used to display a link to the chart"
    )

    def __str__(self):
        return self.name


class ChartConfig(models.Model):
    """A class to store config-info for Charts"""

    label = models.CharField(
        max_length=255, blank=True, help_text="A label of the chart."
    )
    field_path = models.CharField(
        max_length=255, blank=True, help_text="The constructor of to the plotted value."
    )
    chart_types = models.ManyToManyField(
        ChartType, blank=True, help_text="A selection of chart types which should be accessible."
    )
    help_text = models.CharField(
        max_length=255, blank=True, help_text="Contains a description of the chart"
    )
    legend_x = models.CharField(
        max_length=255, blank=True, help_text="Text for the legend of the x-axis"
    )
    legend_y = models.CharField(
        max_length=255, blank=True, help_text="Text for the legend of the y-axis"
    )

    def __str__(self):
        return "{} ({})".format(self.label, self.field_path)
