from rest_framework import serializers
from .models import CarReview, CarReviewImage, CarRating


class CarRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для оценок автомобиля."""

    class Meta:
        model = CarRating
        fields = ("id", "criteria", "score")


class CarReviewImageSerializer(serializers.ModelSerializer):
    """Сериализатор для оценок картинок автомобиля."""
    car_review = serializers.IntegerField(write_only=True)  # Передаем ID, а не объект
    image = serializers.ImageField()  # Обозначаем поле для файла

    class Meta:
        model = CarReviewImage
        fields = ["id", "car_review", "image"]  # Убираем "review", оставляем только ID

    def validate_review_id(self, value):
        """Проверяем, существует ли отзыв с таким ID"""
        if not CarReview.objects.filter(id=value).exists():
            raise serializers.ValidationError("Отзыв с таким ID не найден.")
        return value

    def create(self, validated_data):
        """Создаем объект, связывая с `Review`"""
        review = CarReview.objects.get(id=validated_data.pop("car_review"))
        return CarReviewImage.objects.create(car_review=review, **validated_data)


class CarReviewDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов (выводит всё) автомобиля."""

    ratings = CarRatingSerializer(many=True, read_only=True)  # Оценки (только чтение)
    images = CarReviewImageSerializer(
        many=True, read_only=True, source="car_images"
    )  # Картинки (только чтение)

    class Meta:
        model = CarReview
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


class CarReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для POST/PUT (только отзывы и оценки) автомобиля."""

    ratings = CarRatingSerializer(many=True)  # Позволяет передавать оценки

    class Meta:
        model = CarReview
        fields = ("id", "user", "car", "text", "ratings")

    def create(self, validated_data):
        """Создание отзыва вместе с оценками автомобиля."""
        ratings_data = validated_data.pop("ratings", [])  # Достаём оценки
        review = CarReview.objects.create(**validated_data)  # Создаём отзыв

        # Добавляем оценки
        for rating in ratings_data:
            CarRating.objects.create(car_review=review, **rating)

        return review

    def update(self, instance, validated_data):
        """Обновление отзыва и оценок автомобиля."""
        ratings_data = validated_data.pop("ratings", None)  # Достаём оценки, если есть
        instance.text = validated_data.get("text", instance.text)
        instance.save()

        if ratings_data is not None:
            instance.ratings.all().delete()  # Удаляем старые оценки
            for rating in ratings_data:
                Rating.objects.create(Car_review=instance, **rating)

        return instance
