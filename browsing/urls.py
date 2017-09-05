from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'n3/$', views.EditionN3View.as_view(), name='n3'),
	url(r'xml/$', views.EditionXMLView, name='xml'),
	url(r'bibtex/$', views.EditionBibtextView, name='bibtex'),
    url(r'editions/$', views.EditionListView.as_view(), name='browse_editions'),
    url(r'map/$', views.MapView.as_view(), name='map'),
    url(r'download/$', views.EditionDownloadView.as_view(), name='dl'),
]