from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'list/$', views.EditionListView.as_view(), name='edition_list')
]
