import lxml.etree as ET
from django.conf import settings
import email.utils


NSMAP = {None: "http://www.w3.org/2005/Atom"}
ALTO = "{%s}" % "http://www.w3.org/2005/Atom"


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
    feed = ET.Element('rss', nsmap={'atom': 'http://www.w3.org/2005/Atom'})
    feed.attrib['version'] = "2.0"
    channel = ET.Element('channel')
    title = ET.Element('title')
    title.text = RSS_CHANNEL['title']
    plain_link = ET.Element('link')
    plain_link.text = "{}/rss/feeds/".format(RSS_CHANNEL['link'])
    channel.append(plain_link)
    link = ET.Element('{http://www.w3.org/2005/Atom}link')
    link.attrib['href'] = "{}/rss/feeds/".format(RSS_CHANNEL['link'])
    link.attrib['rel'] = 'self'
    link.attrib['type'] = 'application/rss+xml'
    description = ET.Element('description')
    description.text = RSS_CHANNEL['description']
    channel.append(plain_link)
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
        cleaned_body = x.body.replace('aria-hidden="true"', '')
        i_description.text = cleaned_body
        i_pubdate = ET.Element('pubDate')
        i_pubdate.text = email.utils.format_datetime(x.created)
        i_guid = ET.Element('guid')
        i_guid.text = "{}#{}".format(RSS_CHANNEL['link'], x.id)
        item.append(i_title)
        item.append(i_link)
        item.append(i_description)
        item.append(i_pubdate)
        item.append(i_guid)
        channel.append(item)
    feed.append(channel)
    return feed
