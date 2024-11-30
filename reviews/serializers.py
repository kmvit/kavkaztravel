from rest_framework import serializers
from .models import Review, ReviewPhoto


class ReviewPhotoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для фотографии отзыва.
    """

    class Meta:
        model = ReviewPhoto
        fields = ["image", "caption"]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзыва, который включает вложенные фотографии.
    """

    photos = ReviewPhotoSerializer(many=True, read_only=True)
    content_type_name = (
        serializers.SerializerMethodField()
    )  # Поле для отображения названия модели

    class Meta:
        model = Review
        fields = [
            "id",
            "text",
            "rating",
            "content_type",
            "object_id",
            "photos",
            "content_type_name",
        ]

    def get_content_type_name(self, obj):
        """
        Получение названия модели для поля content_type.
        """
        return obj.content_type.model  # Возвращаем название модели как строку


class ReviewPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзыва, который включает вложенные фотографии.
    """

    photos = ReviewPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ["id", "text", "rating", "content_type", "object_id", "photos"]
