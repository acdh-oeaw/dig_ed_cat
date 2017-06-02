from rest_framework import viewsets
from .serializers import NewsFeedSerializer
from .models import NewsFeed


class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer
