from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework import serializers
from .models import (
    DateTour,
    GalleryTour,
    Geo,
    Guide,
    Order,
    ReviewImageTour,
    ReviewTour,
    Tag,
    Tour,
    TourOperator,
)


class GuideSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Guide.

    Позволяет преобразовывать данные о гиде в формат JSON и обратно.
    Включает информацию о владельце.
    """

    owner = serializers.StringRelatedField(
        read_only=True
    )  # serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Guide
        fields = "__all__"


class TourOperatorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TourOperator.

    Позволяет преобразовывать данные о туроператоре в формат JSON и обратно.
    Включает информацию о владельце.
    """

    owner = serializers.StringRelatedField(
        read_only=True
    )  # serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TourOperator
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели геолокаций тура при get запросе.

    Этот класс отвечает за преобразование экземпляров модели Tag
    в JSON и обратно, а также за валидацию входных данных.
    """

    class Meta:
        model = Tag
        fields = ("id", "name")


class GeoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели геолокаций тура при get запросе.

    Этот класс отвечает за преобразование экземпляров модели Geo
    в JSON и обратно, а также за валидацию входных данных.
    """

    class Meta:
        model = Geo
        fields = ["id", "geo_title", "geo_description"]


class TourGETSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тура при get запросе.

    Этот класс отвечает за преобразование экземпляров модели Tour
    в JSON и обратно, а также за валидацию входных данных.
    """

    tag = TagSerializer()
    tour_operator = serializers.StringRelatedField(read_only=True)
    geo = GeoSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = (
            "id",
            "name",
            "description",
            "geo",
            "tag",
            "tour_operator",
            "slug",
            "rating",
        )

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг тура на основе отзывов, если их нет - возвращает 0."""
        # Получаем тур с аннотированным средним рейтингом
        tour_with_rating = get_object_or_404(
            Tour.objects.annotate(average_rating=Avg("tour__rating")), id=obj.id
        )
        # Если есть отзывы, возвращаем средний рейтинг
        if tour_with_rating.average_rating is not None:
            return round(tour_with_rating.average_rating, 2)

        # Если нет отзывов, возвращаем 0
        return 0


class TourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели  тура.

    Этот класс отвечает за преобразование экземпляров модели Tour
    в JSON и обратно, а также за валидацию входных данных.
    """

    class Meta:
        model = Tour
        fields = ("id", "name", "description", "geo", "tag", "tour_operator", "slug")


class GalleryTourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели изображений тура.

    Этот класс отвечает за преобразование экземпляров модели GalleryTour
    в JSON и обратно, а также за валидацию входных данных.
    """

    tour = TourGETSerializer()

    class Meta:
        model = GalleryTour
        fields = ("id", "tour", "image")


class DateTourrSerializer(serializers.ModelSerializer):
    """Сериализатор для модели даты и дат продолжительности тура.

    Этот класс отвечает за преобразование экземпляров модели DateTour
    в JSON и обратно, а также за валидацию входных данных.
    """

    tour = TourGETSerializer()

    class Meta:
        model = DateTour
        fields = ("id", "tour", "begin_date", "end_date", "is_free")


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели заказа тура.

    Этот класс отвечает за преобразование экземпляров модели Order
    в JSON и обратно, а также за валидацию входных данных.
    """

    class Meta:
        model = Order
        fields = ["id", "tour", "date", "size", "username", "email", "phone"]


class OrderGetSerializer(OrderSerializer):
    """Сериализатор для модели заказа тура.

    Этот класс отвечает за преобразование экземпляров модели Order
    в JSON и обратно, а также за валидацию входных данных.
    """

    tour = TourGETSerializer()


class ReviewImageTourSerializer(serializers.ModelSerializer):
    """Сериализатор для изображения отзыва о турах."""

    class Meta:
        model = ReviewImageTour
        fields = ["id", "image"]


class ReviewTourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.

    Этот класс преобразует экземпляры модели ReviewTour
    в JSON и обратно, а также валидирует входные данные.
    """

    review_images = ReviewImageTourSerializer(many=True, required=False)

    class Meta:
        model = ReviewTour
        fields = ["id", "tour", "owner", "rating", "comment", "date", "review_images"]
