from rest_framework import serializers
from .models import CarReview, CarReviewImage, CarRating


class CarRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для оценок автомобиля."""

    class Meta:
        model = CarRating
        fields = ("id", "criteria", "score")


class CarReviewImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = CarReviewImage
        fields = ["id", "car_review", "image"]


class CarReviewDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов выводит отдельый запрос для автомобиля."""

    ratings = CarRatingSerializer(many=True, read_only=True)
    images = CarReviewImageSerializer(many=True, read_only=True, source="car_images")

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
            "score",
        )


class CarReviewListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка отзывов для одной машины с добавлением среднего рейтинга по критериям.
    """

    images = CarReviewImageSerializer(many=True, read_only=True, source="car_images")

    class Meta:
        model = CarReview
        fields = ("id", "user", "car", "text", "score", "created_at", "images")


class CarReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для POST/PUT (только отзывы и оценки) автомобиля."""

    ratings = CarRatingSerializer(many=True)

    class Meta:
        model = CarReview
        fields = (
            "id",
            "user",
            "car",
            "text",
            "ratings",
            "score",
        )

    def create(self, validated_data):
        """Создание отзыва вместе с оценками автомобиля."""
        ratings_data = validated_data.pop("ratings", [])
        review = CarReview.objects.create(**validated_data)

        for rating in ratings_data:
            CarRating.objects.create(car_review=review, **rating)

        return review

    def update(self, instance, validated_data):
        """Обновление отзыва и оценок автомобиля."""
        ratings_data = validated_data.pop("ratings", None)
        instance.text = validated_data.get("text", instance.text)
        instance.save()

        if ratings_data is not None:
            instance.ratings.all().delete()
            for rating in ratings_data:
                Rating.objects.create(Car_review=instance, **rating)

        return instance
