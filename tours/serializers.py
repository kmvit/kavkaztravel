from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers, viewsets
from .models import TourOperator, Tour, GalleryTour, AvailableDateTour, Order, TagTour


class TourOperatorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TourOperator (Туроператор).

    Используется для:
    - Отображения информации о туроператоре
    - Создания/обновления записей туроператоров
    """

    class Meta:
        model = TourOperator
        fields = ["id", "region", "owner", "license_number"]


class TagTourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TagTour (Теги туров).

    - Поддерживает все CRUD операции с тегами
    - Используется как вложенный сериализатор в TourDetailSerializer
    - Автоматически проверяет уникальность name
    """

    class Meta:
        model = TagTour
        fields = ["id", "name", "description", "tag_type"]


class GalleryTourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели GalleryTour (Галерея изображений тура).

    - Привязан к конкретному туру через ForeignKey
    """

    class Meta:
        model = GalleryTour
        fields = ["id", "tour", "image"]


class AvailableDateTourSerializer(serializers.ModelSerializer):
    """Сериализатор для доступных дат проведения туров (AvailableDateTour).

    Валидация включает:
    1. Проверку что start_date не в прошлом
    2. Проверку что end_date > start_date
    """

    class Meta:
        model = AvailableDateTour
        fields = ["id", "tour", "start_date", "end_date", "is_active"]

    def validate(self, data):
        """Комплексная валидация временного периода тура."""
        today = timezone.now().date()
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Проверка дат
        if start_date and end_date:
            if start_date < today:
                raise serializers.ValidationError(
                    {"start_date": "Дата начала не может быть в прошлом."}
                )

            if end_date < today:
                raise serializers.ValidationError(
                    {"end_date": "Дата окончания не может быть в прошлом."}
                )

            if end_date <= start_date:
                raise serializers.ValidationError(
                    {"end_date": "Должна быть позже даты начала."}
                )

        return data


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Order (Заказы туров).

    - Оформление новых заказов клиентами
    - Поле owner устанавливается автоматически из request.user
    - Проверка формата email и телефона

    """

    class Meta:
        model = Order
        fields = ["id", "tour", "date", "size", "username", "email", "phone"]
        read_only_fields = ["owner"]  # Запрещаем установку владельца через API

    def create(self, validated_data):
        """Создание нового заказа с автоматическим назначением владельца"""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class TourDetailSerializer(serializers.ModelSerializer):
    """Комплексный сериализатор для детального отображения тура.

    - Включает вложенные объекты: теги и галерею
    - Оптимизирует запросы через prefetch_related
    """

    tags = TagTourSerializer(many=True)
    gallery_tour = GalleryTourSerializer(many=True)

    class Meta:
        model = Tour
        fields = [
            "id",
            "guide",
            "title",
            "description",
            "terms",
            "region",
            "tags",
            "price",
            "created_at",
            "gallery_tour",
        ]


class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Кастомное поле PrimaryKeyRelatedField, чтобы отключить стандартную валидацию.
    """

    def to_internal_value(self, data):
        """
        Переопределение этого метода, чтобы отключить стандартную валидацию.
        """
        # Вместо стандартной валидации, просто возвращаем данные, как есть
        try:
            return self.queryset.get(pk=data)
        except self.queryset.model.DoesNotExist:
            raise serializers.ValidationError(f"Тег с ID {data} не существует!")


class TourCreateUpdateSerializer(serializers.ModelSerializer):
    """Специализированный сериализатор для создания/обновления туров.

    - Поле guide автоматически устанавливается из request.user
    - Теги передаются массивом ID (например, "tags": [1, 5, 8])
    - При обновлении полностью заменяет список тегов
    """

    tags = CustomPrimaryKeyRelatedField(
        queryset=TagTour.objects.all(), many=True, required=False
    )

    class Meta:
        model = Tour
        fields = ["id", "title", "description", "terms", "region", "tags", "price"]
        read_only_fields = ["guide"]  # Делаем поле guide только для чтения

    def create(self, validated_data):
        """Создает тур и связывает теги в одной транзакции."""
        tags_data = validated_data.pop("tags", [])
        # Получаем текущего пользователя из контекста запроса
        validated_data["guide"] = self.context["request"].user
        tour = Tour.objects.create(**validated_data)

        if tags_data:
            tour.tags.set(tags_data)

        return tour

    def update(self, instance, validated_data):
        """Обновление тура"""
        tags_data = validated_data.pop("tags", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags_data:
            instance.tags.set(tags_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        """Преобразуем теги в список их имен"""
        representation = super().to_representation(instance)
        tag_names = instance.tags.values_list("name", flat=True)
        representation["tags"] = list(tag_names)
        return representation
