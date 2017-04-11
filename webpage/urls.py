from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start_view, name="start"),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^accounts/login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^imprint/$', views.imprint, name='imprint'),
    url(r'^markdown/$', views.markdown_view, name='markdown'),
    url(r'^documentation/$', views.documentation_view, name='documentation'),
    url(r'^survey/$', views.survey_view, name='survey'),
    url(r'^faq/$', views.faq_view, name='faq'),
]
