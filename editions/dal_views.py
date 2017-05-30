from dal import autocomplete
from .models import *
from django.db.models import Q


class PersonAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Person.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class InstitutionAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Institution.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class EditionAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Edition.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
