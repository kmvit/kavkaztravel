from rest_framework import serializers
from .models import (
    DateTour,
    EstimationTour,
    GalleryTour,
    Geo,
    Guide,
    Order,
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

    class Meta:
        model = Tour
        fields = ("id", "name", "description", "geo", "tag", "tour_operator", "slug")


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


class EstimationTourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.

    Этот класс преобразует экземпляры модели EstimationTour
    в JSON и обратно, а также валидирует входные данные.
    """

    class Meta:
        model = EstimationTour
        fields = ["id", "tour", "estimation", "feedback", "image"]


class EstimationTourGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.

    Этот класс преобразует экземпляры модели EstimationTour
    в JSON и обратно, а также валидирует входные данные.
    """

    rating = serializers.SerializerMethodField()
    tour = TourGETSerializer()

    class Meta:
        model = EstimationTour
        fields = ["id", "tour", "estimation", "feedback", "image", "date", "rating"]

    def get_rating(self, obj):
        """
        Функция предназначена для получения рейтинга тура.

        Значение передаеться в поле "rating"
        Рассчитываеться как сумма всех оценок тура
        деленная на количество отзывов. По умолчанию оценка равна 10.
        """
        estimations = EstimationTour.objects.filter(tour=obj.tour)
        total_estimation = len(estimations)
        sum_estimation = sum(est.estimation for est in estimations)
        if total_estimation > 0:
            return round(sum_estimation / total_estimation, 2)
        return 10
