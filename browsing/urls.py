from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'editions/$', views.EditionListView.as_view(), name='browse_editions'), 
]
