from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers
from .models import Entertainment, ReviewEntertainment, ReviewImageEntertainment


class EntertainmentSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Entertainment
        fields = "__all__"

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг тура на основе отзывов, если их нет - возвращает 0."""
        # Получаем тур с аннотированным средним рейтингом
        entertainment_with_rating = get_object_or_404(
            Entertainment.objects.annotate(average_rating=Avg("entertainment__rating")),
            id=obj.id,
        )
        # Если есть отзывы, возвращаем средний рейтинг
        if entertainment_with_rating.average_rating is not None:
            return round(entertainment_with_rating.average_rating, 2)


class ReviewImageEntertainmentSerializer(serializers.ModelSerializer):
    """Сериализатор для изображения отзыва о гостинице"""
    
    class Meta:
        model = ReviewImageEntertainment
        fields = ['id', 'image']


class ReviewEntertainmentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов о развлечениях или местах отдыха.

    Этот класс преобразует экземпляры модели ReviewEntertainment
    в JSON и обратно, а также валидирует входные данные.
    """

    review_images = ReviewImageEntertainmentSerializer(many=True, required=False)

    class Meta:
        model = ReviewEntertainment
        fields = ["id", "entertainment", "owner", "rating", "comment", "date", "review_images"]
