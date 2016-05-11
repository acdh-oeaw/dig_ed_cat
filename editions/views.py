from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from .models import Edition
from .forms import EditionForm


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


@login_required
def edit_edition(request, pk):
    instance = get_object_or_404(Edition, id=pk)
    if request.method == "POST":
        form = EditionForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('editions:edition_detail', pk=pk)
        else:
            return render(request, 'editions/edit_edition.html', {'form': form})
    else:
        form = EditionForm(instance=instance)
        return render(request, 'editions/edit_edition.html', {'form': form})
