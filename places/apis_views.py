from rest_framework import viewsets
from .serializers import PlaceSerializer, AlternativeNameSerializer
from .models import Place, AlternativeName


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    depth = 2


class AlternativNameViewSet(viewsets.ModelViewSet):
    queryset = AlternativeName.objects.all()
    serializer_class = AlternativeNameSerializer

