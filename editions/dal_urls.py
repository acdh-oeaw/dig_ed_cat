from django.conf.urls import url
from . import views
from . import dal_views
from .models import Person, Institution

app_name = 'editions'

urlpatterns = [
    url(
        r'^person-ac/$',
        dal_views.PersonAC.as_view(),
        name='person-ac',
    ),
    url(
        r'^institution-ac/$',
        dal_views.InstitutionAC.as_view(),
        name='institution-ac',
    ),
    url(
        r'^edition-ac/$',
        dal_views.EditionAC.as_view(),
        name='edition-ac',
    ),
]
