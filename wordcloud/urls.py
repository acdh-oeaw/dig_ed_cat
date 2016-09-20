from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^show/$', views.show, name='show'),
    url(r'^titlewordsjs/$', views.titlewords_js, name='titlewords_js'),
    url(r'^infrastructurejs/$', views.infrastructure_js, name='infrastructure_js'),
]
