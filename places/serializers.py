from rest_framework import serializers
from .models import Place, AlternativeName


class AlternativeNameSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = "__all__"
        model = AlternativeName


class PlaceHelperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = "__all__"
        model = Place


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    alternative_name = AlternativeNameSerializer(many=True)
    part_of = PlaceHelperSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = Place
