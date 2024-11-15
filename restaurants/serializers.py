from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import Avg

from .models import Restaurant, ReviewRestaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Restaurant.

    Позволяет преобразовывать данные о ресторане в формат JSON и обратно.
    Включает информацию о владельце, отзывах и рейтинге ресторана.
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг ресторана на основе отзывов, если их нет - возвращает 0."""
        # Сначала получаем ресторан с аннотированным средним рейтингом
        restaurant_with_rating = (
            Restaurant.objects.annotate(
                average_rating=Avg("restaurant__rating")  # Используем правильную связь
            )
            .filter(id=obj.id)
            .first()
        )

        # Если ресторан найден и есть отзывы, возвращаем средний рейтинг
        if restaurant_with_rating and restaurant_with_rating.average_rating is not None:
            return round(restaurant_with_rating.average_rating, 2)

        # Если ресторан не найден или нет отзывов, возвращаем 0
        return 0


class ReviewRestaurantSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.

    Этот класс преобразует экземпляры модели ReviewRestaurant
    """

    class Meta:
        model = ReviewRestaurant
        fields = ["id", "restaurant", "rating", "comment", "image"]


class ReviewRestaurantGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.

    Этот класс преобразует экземпляры модели ReviewRestaurant
    в JSON и обратно, а также валидирует входные данные.
    """

    owner = serializers.StringRelatedField(read_only=True)
    restaurant = RestaurantSerializer()

    class Meta:
        model = ReviewRestaurant
        fields = ["id", "restaurant", "image", "owner", "rating", "comment", "date"]
