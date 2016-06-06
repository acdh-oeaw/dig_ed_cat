import requests, re, json

from django.shortcuts import (render, render_to_response, get_object_or_404,
	redirect)
from django.views import generic
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Place
from .forms import PlaceForm


class PlaceListView(generic.ListView):
    template_name ="places/list_places.html"
    context_object_name = 'object_list'

	def get_queryset(self):
		return Place.objects.all()


@login_required
def create_place(request):
	if request.method == "POST":
		form = PlaceForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('places:place_list')
		else:
			return render(request, 'places/edit_places.html', {'form':form})
	else:
		form = PlaceForm()
		return render(request, 'places/edit_places.html', {'form':form})

@login_required
def edit_place(request, pk):
    instance = Place.objects.get(id=pk)
    username = "&username=digitalarchiv"
    if request.method == "GET":
        placeName = instance.name
        root = "http://api.geonames.org/searchJSON?q="
        params = "&fuzzy=0.6&lang=en&maxRows=100"
        url = root+placeName+params+username
        try:
            r = requests.get(url)
            response = r.text
            responseJSON = json.loads(response)
            responseJSON = responseJSON['geonames']
            form = PlaceForm(instance = instance)
            print(url)
            return render(
                request, 'places/edit_places.html',
                {'object':instance, 'form':form, 'responseJSON':responseJSON}
            )
        except requests.exceptions.RequestException as e:
            url = e
        form = PlaceForm(instance = instance)
        print(url)
        responseJSON = "hansi"
		#form = OrtForm({'geonames_id':123})
        return render(request, 'places/edit_places.html',
			{'object':instance, 'form':form, 'responseJSON':responseJSON}
			)
    else:
        form = PlaceForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
        return redirect('places:place_list')


class PlaceDelete(DeleteView):
    model = Place
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('places:place_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlaceDelete, self).dispatch(*args, **kwargs)
