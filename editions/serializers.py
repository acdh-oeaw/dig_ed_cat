from rest_framework import serializers
from places.serializers import PlaceSerializer
from .models import Institution, Edition, Person, Period, Language


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    place = PlaceSerializer(many=False)

    class Meta:
        model = Institution


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Person


class PeriodSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Period


class LanguageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Language


class EditionSerializer(serializers.HyperlinkedModelSerializer):

    historical_period = PeriodSerializer(many=True)
    language = LanguageSerializer(many=True)
    manager = PersonSerializer(many=True)
    institution = InstitutionSerializer(many=True)

    class Meta:
        model = Edition
