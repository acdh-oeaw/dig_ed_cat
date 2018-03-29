import lxml.etree as ET
from django.conf import settings


try:
    RSS_CHANNEL = settings.RSS_CHANNEL
except AttributeError:
    RSS_CHANNEL = {
        'title': "provide some",
        'link': "https://some/link",
        'description': "some description",
    }


def feed_serializer(channel_dict, items):
    """takes a channel dictionary and a list of feed items and returns a rss-xml"""
    feed = ET.Element('rss')
    feed.attrib['version'] = "2.0"
    channel = ET.Element('channel')
    title = ET.Element('titel')
    title.text = RSS_CHANNEL['title']
    link = ET.Element('link')
    link.text = RSS_CHANNEL['link']
    description = ET.Element('description')
    description.text = RSS_CHANNEL['description']
    channel.append(title)
    channel.append(link)
    channel.append(description)
    for x in items:
        item = ET.Element('item')
        i_title = ET.Element('title')
        i_title.text = x.title
        i_link = ET.Element('link')
        i_link.text = RSS_CHANNEL['link']
        i_description = ET.Element('description')
        i_description.text = x.body
        i_pubdate = ET.Element('pubDate')
        i_pubdate.text = "{:%A, %d %B %Y %H:%M:%S %Z}".format(x.created)
        i_guide = ET.Element('guide')
        i_guide.text = "{}#{}".format(RSS_CHANNEL['link'], x.id)
        item.append(i_title)
        item.append(i_link)
        item.append(i_description)
        item.append(i_pubdate)
        item.append(i_guide)
        channel.append(item)
    feed.append(channel)
    return feed
