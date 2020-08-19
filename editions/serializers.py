from rest_framework import serializers
from places.serializers import PlaceSerializer
from .models import Institution, Edition, Person, Period, Language


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    place = PlaceSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = Institution


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = "__all__"
        model = Person


class PeriodSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = "__all__"
        model = Period


class LanguageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = "__all__"
        model = Language


class EditionSerializer(serializers.HyperlinkedModelSerializer):

    historical_period = PeriodSerializer(many=True)
    language = LanguageSerializer(many=True)
    manager = PersonSerializer(many=True)
    institution = InstitutionSerializer(many=True)
    handle_pid = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Edition

    def get_handle_pid(self, obj):
        return f"{obj.pid.all().first()}"
