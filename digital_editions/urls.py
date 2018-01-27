from django.conf.urls import url, include, handler404
from django.contrib import admin
from rest_framework import routers
from editions.api_views import (
    InstitutionViewSet, PeriodViewSet, PersonViewSet, LanguageViewSet, EditionViewSet)
from places.apis_views import PlaceViewSet, AlternativNameViewSet
from news.api_views import NewsFeedViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'alternativenames', AlternativNameViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'editions', EditionViewSet)
router.register(r'newsfeeds', NewsFeedViewSet)
router.register(r'users', UserViewSet, base_name='user')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^sparql/', include('sparql.urls', namespace='sparql')),
    url(r'editions/', include('editions.urls', namespace='editions')),
    url(r'^editions-ac/', include('editions.dal_urls', namespace='editions-ac')),
    url(r'places/', include('places.urls', namespace='places')),
    url(r'browsing/', include('browsing.urls', namespace='browsing')),
    url(r'charts/', include('charts.urls', namespace='charts')),
    url(r'wordclouds/', include('wordcloud.urls', namespace='wordclouds')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]

handler404 = 'webpage.views.handler404'
