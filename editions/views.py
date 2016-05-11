from django.shortcuts import render
from django.views import generic

from .models import Edition


class EditionListView(generic.ListView):
    template_name = "editions/list_editions.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return Edition.objects.all()
