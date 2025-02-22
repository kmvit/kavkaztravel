from rest_framework import serializers
from .models import Car, CarFeature, RentalCondition, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений автомобиля."""
    image = serializers.ImageField(use_url=True) 
    class Meta:
        model = CarImage
        fields = ['id', 'car', 'image']


class CarFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик автомобиля."""


    class Meta:
        model = CarFeature
        fields = ['id', 'car', 'name']


class RentalConditionSerializer(serializers.ModelSerializer):
    """Сериализатор для условий аренды автомобиля."""
    
    class Meta:
        model = RentalCondition
        fields = [
            'id',
            'car',
            'insurance_deposit',
            'required_documents',
            'min_driver_age',
            'min_driving_experience',
            'rental_start_date',
            'rental_end_date'
        ]


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для автомобилей, включая характеристики, изображения и условия аренды."""
    owner = serializers.StringRelatedField(read_only=True)  # Отображает имя владельца вместо ID
    features = CarFeatureSerializer(many=True, read_only=True)  # Вложенные характеристики
    images = CarImageSerializer(many=True, read_only=True)  # Вложенные изображения
   

    class Meta:
        model = Car
        fields = [
            'id',
            'owner',
            'brand',
            'body_type',
            'price_per_day',
            'features',
            'images',
            'rental_condition'
        ]
