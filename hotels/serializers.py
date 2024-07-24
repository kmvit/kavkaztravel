from rest_framework import serializers
from .models import Hotel, Tag, HotelImage, RoomImage, Room, RoomPrice, \
    Amenity, AccommodationType, MealPlan
from reviews.serializers import ReviewSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['id', 'name', 'description']


class AccommodationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationType
        fields = ['id', 'name', 'description']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image']


class RoomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPrice
        fields = ['id', 'date', 'price', 'season']


class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    prices = RoomPriceSerializer(many=True, read_only=True)
    hotel = serializers.ReadOnlyField(source='hotel.name')

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'name', 'description', 'capacity', 'images',
                  'prices']


class HotelImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__'
        read_only_fields = ['image']


class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
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
        fields = '__all__'

    def get_rating(self, obj):
        return obj.calculate_rating()
