from django.http import HttpResponse
from news.rss_serializer import RSS_CHANNEL, feed_serializer
import lxml.etree as ET
from .models import NewsFeed


def feed_view(request):
    feeds = feed_serializer(RSS_CHANNEL, NewsFeed.objects.all())
    feed_string = ET.tostring(feeds)
    return HttpResponse(feed_string, content_type='application/xml; charset=utf-8')
