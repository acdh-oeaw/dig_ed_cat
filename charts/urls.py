from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^barcharts/$', views.barcharts_view, name='bar_charts'),
    url(r'^testjson/$', views.test_json, name='test_json'),
    url(r'^piecharts/$', views.piecharts_view, name='pie_charts'),
    url(r'^testjsonpie/$', views.test_json_pie, name='test_json_pie'),
    url(r'^historicalperiodsjson/$', views.historical_periode_json, name='historical_periode_json'),
    url(r'^xmlteijson/$', views.xmltei_json, name='xmltei_json'),
    url(r'^xmldownloadjson/$', views.xmldownload_json, name='xmldownload_json'),
    url(r'^ccjson/$', views.cc_json, name='cc_json'),
    url(r'^searchjson/$', views.search_json, name='search_json'),
    url(r'^advancedsearchjson/$', views.advanced_search_json, name='advanced_search_json'),
    url(r'^indicesjson/$', views.indices_json, name='indices_json'),

]
