from rest_framework import serializers
from .models import Restaurant
from reviews.serializers import ReviewSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Restaurant.
    
    Позволяет преобразовывать данные о ресторане в формат JSON и обратно. 
    Включает информацию о владельце, отзывах и рейтинге ресторана.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг ресторана на основе отзывов."""
        return obj.calculate_rating()
