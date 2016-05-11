from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Edition


class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EditionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'save'))
