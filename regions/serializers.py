from rest_framework import serializers

from reviews.serializers import ReviewSerializer
from .models import Region
from hotels.serializers import HotelSerializer
from restaurants.serializers import RestaurantSerializer
from attractions.serializers import AttractionSerializer
from entertainments.serializers import EntertainmentSerializer


class RegionSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)
    restaurants = RestaurantSerializer(many=True, read_only=True)
    attractions = AttractionSerializer(many=True, read_only=True)
    entertainments = EntertainmentSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = "__all__"

    def get_rating(self, obj):
        return obj.calculate_rating()
