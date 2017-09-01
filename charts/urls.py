from django.conf.urls import url
from . import views, ml_views

urlpatterns = [
    url(r'^chartselector/$', views.ChartSelector.as_view(), name='chart_selector'),
    url(
        r'^chart/(?P<property>[\w\-]+)/(?P<charttype>[\w\-]+)/$',
        views.DynChartView.as_view(), name='dynchart'
    ),
    url(r'^barcharts/$', views.barcharts_view, name='bar_charts'),
    url(r'^testjson/$', views.test_json, name='test_json'),
    url(r'^facsjson/$', views.facs_json, name='facs_json'),
    url(r'^piecharts/$', views.piecharts_view, name='pie_charts'),
    url(r'^testjsonpie/$', views.test_json_pie, name='test_json_pie'),
    url(r'^historicalperiodsjson/$', views.historical_periode_json, name='historical_periode_json'),
    url(r'^xmlteijson/$', views.xmltei_json, name='xmltei_json'),
    url(r'^xmldownloadjson/$', views.xmldownload_json, name='xmldownload_json'),
    url(r'^ccjson/$', views.cc_json, name='cc_json'),
    url(r'^searchjson/$', views.search_json, name='search_json'),
    url(r'^advancedsearchjson/$', views.advanced_search_json, name='advanced_search_json'),
    url(r'^indicesjson/$', views.indices_json, name='indices_json'),
    url(r'^editionspercountryjson/$', views.editions_per_country_json,
        name='editions_per_country_json'),
    url(r'^kmeansjson/$', ml_views.kmeans_json, name='kmeans_json'),
]
