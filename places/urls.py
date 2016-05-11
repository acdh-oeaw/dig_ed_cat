from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^list/$', views.PlaceListView.as_view(), name='place_list'),
url(r'^create/$', views.create_place, name='place_create'),
url(r'^edit/(?P<pk>[0-9]+)$', views.edit_place, name='place_edit'),
url(r'^delete/(?P<pk>[0-9]+)$', views.PlaceDelete.as_view(), name='place_delete')
]