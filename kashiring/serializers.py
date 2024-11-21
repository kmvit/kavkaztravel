from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import Avg
from .models import Brand, Model, ReviewAuto, ReviewImageAuto, Year, Color, BodyType, Auto, Company


class BrandSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Brand.

    Обеспечивает преобразование данных бренда автомобиля в формат JSON и обратно.
    """

    class Meta:
        model = Brand
        fields = "__all__"


class ModelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Model.

    Обеспечивает преобразование данных модели автомобиля в формат JSON и обратно.
    """

    class Meta:
        model = Model
        fields = "__all__"


class YearSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Year.

    Представляет год выпуска автомобиля.
    """

    class Meta:
        model = Year
        fields = ("year",)


class ColorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Color.

    Обеспечивает преобразование данных цвета автомобиля в формат JSON и обратно.
    """

    class Meta:
        model = Color
        fields = "__all__"


class BodyTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели BodyType.

    Обеспечивает преобразование данных типа кузова автомобиля в формат JSON и обратно.
    """

    class Meta:
        model = BodyType
        fields = "__all__"


class AutoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и изменения объектов модели Auto.

    Обеспечивает преобразование данных автомобиля в формат JSON и обратно.
    Поля, связанные с брендом, моделью, годом, цветом и типом кузова, доступны только для чтения.
    """

    brand = serializers.PrimaryKeyRelatedField(read_only=True)
    model = serializers.PrimaryKeyRelatedField(read_only=True)
    year = serializers.PrimaryKeyRelatedField(read_only=True)
    color = serializers.PrimaryKeyRelatedField(read_only=True)
    body_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Auto
        fields = "__all__"

    def to_representation(self, instance):
        """
        Переопределяет метод to_representation для удаления полей с null значениями.
        """
        representation = super().to_representation(instance)
        # Удаляем ключи, значения которых равны None
        return {
            key: value for key, value in representation.items() if value is not None
        }


class AutoGETSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения данных об автомобиле.

    Включает преобразование полей, связанных с брендом и моделью, в строковые представления.
    """

    brand = serializers.StringRelatedField(read_only=True)
    model = serializers.StringRelatedField(read_only=True)
    year = YearSerializer()
    color = serializers.StringRelatedField(read_only=True)
    body_type = serializers.StringRelatedField(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Auto
        fields = ("id", "brand", "model", "year", "color", "body_type", "rating")

    def to_representation(self, instance):
        """
        Переопределяет метод to_representation для удаления полей с null значениями.
        """
        representation = super().to_representation(instance)
        # Удаляем ключи, значения которых равны None
        return {
            key: value for key, value in representation.items() if value is not None
        }

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг тура на основе отзывов, если их нет - возвращает 0."""
        # Получаем тур с аннотированным средним рейтингом
        auto_with_rating = get_object_or_404(
            Auto.objects.annotate(average_rating=Avg("auto__rating")), id=obj.id
        )
        # Если есть отзывы, возвращаем средний рейтинг
        if auto_with_rating.average_rating is not None:
            return round(auto_with_rating.average_rating, 2)


class AutoMiniSerializer(serializers.ModelSerializer):
    """
    Мини-сериализатор для модели Auto.

    Представляет минимальный набор данных об автомобиле, включая бренд и модель.
    """

    brand = serializers.StringRelatedField(read_only=True)
    model = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Auto
        fields = (
            "id",
            "brand",
            "model",
        )


class CompanyAutoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения информации о компании и связанных с ней автомобилях.
    """

    auto = AutoMiniSerializer(many=True)

    class Meta:
        model = Company
        fields = (
            "name",
            "auto",
        )


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Company.

    Представляет информацию о компании, включая ее название.
    """

    class Meta:
        model = Company
        fields = ("name",)


class ReviewAutoHotelSerializer(serializers.ModelSerializer):
    """Сериализатор для изображения отзыва о машинах."""
    
    class Meta:
        model = ReviewImageAuto
        fields = ['id', 'image']
        


class ReviewAutoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов машин для каширинга.

    Этот класс преобразует экземпляры модели ReviewAuto
    """
    review_images = ReviewAutoHotelSerializer(many=True, required=False)
    class Meta:
        model = ReviewAuto
        fields = ['id', 'auto', 'owner', 'rating', 'comment', 'date', 'review_images']

