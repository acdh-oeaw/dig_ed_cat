from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'editions/$', views.EditionListView.as_view(), name='browse_editions'),
    url(r'map/$', views.MapView.as_view(), name='map'),
    url(r'download/$', views.EditionDownloadView.as_view(), name='dl'),
]
