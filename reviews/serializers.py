from rest_framework import serializers
from .models import Review, ReviewImage, Rating


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор для оценок"""

    class Meta:
        model = Rating
        fields = ("id", "criteria", "score")


class ReviewImageSerializer(serializers.ModelSerializer):
    review_id = serializers.IntegerField(write_only=True)  # Передаем ID, а не объект
    image = serializers.ImageField()  # Обозначаем поле для файла

    class Meta:
        model = ReviewImage
        fields = ["id", "review_id", "image"]  # Убираем "review", оставляем только ID

    def validate_review_id(self, value):
        """Проверяем, существует ли отзыв с таким ID"""
        if not Review.objects.filter(id=value).exists():
            raise serializers.ValidationError("Отзыв с таким ID не найден.")
        return value

    def create(self, validated_data):
        """Создаем объект, связывая с `Review`"""
        review = Review.objects.get(id=validated_data.pop("review_id"))
        return ReviewImage.objects.create(review=review, **validated_data)


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов (выводит всё)"""

    ratings = RatingSerializer(many=True, read_only=True)  # Оценки (только чтение)
    images = ReviewImageSerializer(
        many=True, read_only=True
    )  # Картинки (только чтение)

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "car",
            "text",
            "created_at",
            "is_approved",
            "ratings",
            "images",
        )


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для POST/PUT (только отзывы и оценки)"""

    ratings = RatingSerializer(many=True)  # Позволяет передавать оценки

    class Meta:
        model = Review
        fields = ("id", "user", "car", "text", "ratings")

    def create(self, validated_data):
        """Создание отзыва вместе с оценками"""
        ratings_data = validated_data.pop("ratings", [])  # Достаём оценки
        review = Review.objects.create(**validated_data)  # Создаём отзыв

        # Добавляем оценки
        for rating in ratings_data:
            Rating.objects.create(review=review, **rating)

        return review

    def update(self, instance, validated_data):
        """Обновление отзыва и оценок"""
        ratings_data = validated_data.pop("ratings", None)  # Достаём оценки, если есть
        instance.text = validated_data.get("text", instance.text)
        instance.save()

        if ratings_data is not None:
            instance.ratings.all().delete()  # Удаляем старые оценки
            for rating in ratings_data:
                Rating.objects.create(review=instance, **rating)

        return instance
