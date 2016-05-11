from django.views import generic
from django.views.generic.detail import DetailView

from .models import Edition


class EditionListView(generic.ListView):
    template_name = "editions/list_editions.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        return Edition.objects.all()


class EditionDetailView(DetailView):
    model = Edition

    def get_context_data(self, **kwargs):
        context = super(EditionDetailView, self).get_context_data(**kwargs)

        return context
