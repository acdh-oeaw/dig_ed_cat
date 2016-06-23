from rest_framework import serializers
from .models import Place, AlternativeName


class AlternativeNameSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AlternativeName


class PlaceHelperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Place


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    alternative_name = AlternativeNameSerializer(many=True)
    part_of = PlaceHelperSerializer(many=False)

    class Meta:
        model = Place
