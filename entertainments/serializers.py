from rest_framework import serializers
from .models import Entertainment
from reviews.serializers import ReviewSerializer


class EntertainmentSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Entertainment
        fields = "__all__"

    def get_rating(self, obj):
        return obj.calculate_rating()
