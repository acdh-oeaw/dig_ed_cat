from django.conf.urls import url
from . import views

app_name = 'browsing'

urlpatterns = [
    url(r'rdf/$', views.EditionRDFView.as_view(), name='rdf'),
    url(r'xml/$', views.EditionXMLView, name='xml'),
    url(r'bibtex/$', views.EditionBibtextView, name='bibtex'),
    url(r'editions/$', views.EditionListView.as_view(), name='browse_editions'),
    url(r'map/$', views.MapView.as_view(), name='map'),
    url(r'netvis/$', views.NetVisView.as_view(), name='netvis'),
    url(r'download/$', views.EditionDownloadView.as_view(), name='dl'),
    url(r'netvis-json/$', views.NetVisDownloadJSONView.as_view(), name='netvisjson'),
]
