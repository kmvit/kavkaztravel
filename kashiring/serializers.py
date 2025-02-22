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
    """Сериализатор для просмотра автомобилей с характеристиками и изображениями."""
    owner = serializers.StringRelatedField(read_only=True)
    features = CarFeatureSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)

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
        ]


class CarFeatureCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления характеристик автомобиля."""

    class Meta:
        model = CarFeature
        fields = ['name']


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления автомобиля с вложенными характеристиками."""

    features = CarFeatureCreateUpdateSerializer(many=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'owner',
            'brand',
            'body_type',
            'price_per_day',
            'features',
        ]

    def create(self, validated_data):
        """Создаем автомобиль и его характеристики."""

        # Получаем характеристики, если они есть
        features_data = validated_data.pop('features', [])

        # Создаем сам автомобиль
        car = Car.objects.create(**validated_data)

        # Сохраняем характеристики
        for feature_data in features_data:
            CarFeature.objects.create(car=car, **feature_data)

        return car

    def update(self, instance, validated_data):
        """Обновляем данные автомобиля и его характеристики."""

        # Получаем обновленные характеристики, если они есть
        features_data = validated_data.pop('features', [])

        # Обновляем автомобиль
        instance.brand = validated_data.get('brand', instance.brand)
        instance.body_type = validated_data.get('body_type', instance.body_type)
        instance.price_per_day = validated_data.get('price_per_day', instance.price_per_day)
        instance.save()

        # Обновляем или добавляем новые характеристики
        for feature_data in features_data:
            CarFeature.objects.update_or_create(car=instance, **feature_data)

        return instance
