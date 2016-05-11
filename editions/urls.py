from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'list/$', views.EditionListView.as_view(), name='edition_list'),
    url(r'^detail/(?P<pk>[0-9]+)$', views.EditionDetailView.as_view(), name='edition_detail')
]
