from django import template
from news.models import NewsFeed

register = template.Library()


@register.inclusion_tag('news/newsfeed.html')
def newsfeed():
    feeds = NewsFeed.objects.all()
    return {'feeds': feeds}


@register.inclusion_tag('news/newsfeed.html')
def newsfeed_last_items(amount=None):
    if amount is None:
        feeds = NewsFeed.objects.all()
    else:
        feeds = NewsFeed.objects.all()[0:amount]
    return {'feeds': feeds}
