from rest_framework import serializers
from .models import NewsFeed


class NewsFeedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        exclude = ['author']
        model = NewsFeed
