from rest_framework import serializers
from .models import Region
from hotels.serializers import HotelSerializer
from restaurants.serializers import RestaurantSerializer

from entertainments.serializers import EntertainmentSerializer


class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Region.

    Позволяет преобразовывать данные региона в формат JSON и обратно, включая связанные
    объекты, такие как отели, рестораны, аттракционы и развлечения.
    """

    hotels = HotelSerializer(many=True, read_only=True)
    restaurants = RestaurantSerializer(many=True, read_only=True)
    entertainments = EntertainmentSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = "__all__"

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг региона на основе отзывов."""
        return obj.calculate_rating()
