# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ['alternative_name']
        fields = ['name', 'geonames_id', 'lat', 'lng', 'part_of', 'place_type']

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
