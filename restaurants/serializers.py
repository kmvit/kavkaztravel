from rest_framework import serializers
from django.db.models import Avg

from .models import Restaurant, ReviewImageRestaurant, ReviewRestaurant


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


class ReviewImageRestaurantSerializer(serializers.ModelSerializer):
    """Сериализатор для изображения отзыва о местах общественного питания."""
    
    class Meta:
        model = ReviewImageRestaurant
        fields = ['id', 'image']


class ReviewRestaurantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзыва о местах общественного питания
    с вложенными изображениями.
    """
    
    review_images = ReviewImageRestaurantSerializer(many=True, required=False)

    class Meta:
        model = ReviewRestaurant
        fields = ['id', 'restaurant', 'owner', 'rating', 'comment', 'date', 'review_images']
