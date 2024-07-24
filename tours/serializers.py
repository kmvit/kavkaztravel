from rest_framework import serializers
from .models import Guide, TourOperator


class GuideSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Guide
        fields = '__all__'


class TourOperatorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TourOperator
        fields = '__all__'
