from django import template
from webpage.metadata import PROJECT_METADATA as PM

register = template.Library()


@register.simple_tag
def projects_metadata(key):
    return PM[key]
