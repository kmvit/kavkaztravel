from rest_framework import serializers
from .models import Restaurant
from reviews.serializers import ReviewSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_rating(self, obj):
        return obj.calculate_rating()
