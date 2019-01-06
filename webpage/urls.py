from django.conf.urls import url
from . import views

app_name = 'webpage'

urlpatterns = [
    url(r'^$', views.GenericWebpageView.as_view(), name="start"),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^accounts/login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^project-info/$', views.project_info, name='project_info'),
    url(r'^(?P<template>[\w-]+)/$', views.GenericWebpageView.as_view(), name='staticpage'),
]
