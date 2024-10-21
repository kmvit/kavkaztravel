from rest_framework import serializers
from .models import Attraction
from reviews.serializers import ReviewSerializer


class AttractionSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = "__all__"

    def get_rating(self, obj):
        return obj.calculate_rating()
