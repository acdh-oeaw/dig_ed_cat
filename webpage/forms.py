# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div


class form_user_login(forms.Form):
	username = forms.CharField(label='Username',widget=forms.TextInput)
	password = forms.CharField(label='Password',widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(form_user_login, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.add_input(Submit('submit','Login'))