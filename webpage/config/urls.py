from django.conf.urls import url, include
from django.contrib import admin
from autocomplete_light import shortcuts as al
al.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('webpage.urls', namespace='webpage')),