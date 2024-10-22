from rest_framework import serializers
from .models import (
    Hotel,
    Tag,
    HotelImage,
    RoomImage,
    Room,
    RoomPrice,
    Amenity,
    AccommodationType,
    MealPlan,
)
from reviews.serializers import ReviewSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag. 
    Обеспечивает преобразование данных тегов, позволяя работать с ними в формате JSON.
    """
    class Meta:
        model = Tag
        fields = "__all__"


class MealPlanSerializer(serializers.ModelSerializer):
    """Сериализатор для модели MealPlan. 
    Представляет меню питания, включая их названия и описания.
    """
    class Meta:
        model = MealPlan
        fields = ["id", "name", "description"]


class AccommodationTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели AccommodationType. 
    Описывает типы размещения.
    """
    class Meta:
        model = AccommodationType
        fields = ["id", "name", "description"]


class AmenitySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Amenity. 
    Описывает удобства, доступные в отеле.
    """
    class Meta:
        model = Amenity
        fields = ["id", "name", "description"]


class RoomImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели RoomImage. 
    Отвечает за преобразование изображений, связанных с номерами.
    """
    class Meta:
        model = RoomImage
        fields = ["id", "image"]


class RoomPriceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели RoomPrice. 
    Представляет информацию о ценах на номера, включая дату и сезон.
    """
    class Meta:
        model = RoomPrice
        fields = ["id", "date", "price", "season"]


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Room. 
    Включает информацию о номерах, а также связанные изображения и цены.
    """
    images = RoomImageSerializer(many=True, read_only=True)
    prices = RoomPriceSerializer(many=True, read_only=True)
    hotel = serializers.ReadOnlyField(source="hotel.name")

    class Meta:
        model = Room
        fields = ["id", "hotel", "name", "description", "capacity", "images", "prices"]


class HotelImageSerializers(serializers.ModelSerializer):
    """Сериализатор для модели HotelImage. 
    Отвечает за преобразование изображений отелей.
    """
    class Meta:
        model = HotelImage
        fields = "__all__"
        read_only_fields = ["image"]


class HotelSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Hotel. 
    Представляет полную информацию об отеле, включая номера, отзывы, рейтинг, удобства и планы питания.
    """
    owner = serializers.ReadOnlyField(source="owner.username")
    rooms = RoomSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    images = HotelImageSerializers(many=True)
    meal_plan = MealPlanSerializer(many=True, read_only=True)
    accommodation_type = AccommodationTypeSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = "__all__"

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг 
        отеля на основе его отзывов."""
        return obj.calculate_rating()
