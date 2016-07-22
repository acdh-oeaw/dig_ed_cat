from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from editions.api_views import (
    InstitutionViewSet, PeriodViewSet, PersonViewSet, LanguageViewSet, EditionViewSet)
from places.apis_views import PlaceViewSet, AlternativNameViewSet

router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'alternativenames', AlternativNameViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'editions', EditionViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('webpage.urls', namespace='webpage')),
    url(r'editions/', include('editions.urls', namespace='editions')),
    url(r'places/', include('places.urls', namespace='places')),
    url(r'^datamodel/', include('django_spaghetti.urls', namespace='datamodel')),
    url(r'browsing/', include('browsing.urls', namespace='browsing')),
    url(r'charts/', include('charts.urls', namespace='charts'))
]
