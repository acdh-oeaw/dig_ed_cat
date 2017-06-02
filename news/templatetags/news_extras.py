from django import template
from news.models import NewsFeed

register = template.Library()


@register.inclusion_tag('news/newsfeed.html')
def newsfeed(number_of_feeds=5):
    feeds = NewsFeed.objects.all()
    return {'feeds': feeds}
