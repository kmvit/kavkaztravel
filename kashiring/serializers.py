from rest_framework import serializers
from .models import (
    Car,
    CarFeature,
    CarImage,
    RentalDiscount,
    Rental,
    RentalCondition,
    Brand,
    CarOption,
    CarEquipment,
    Model,
)
from reviews.models import Car, CarReview 

class ModelSerializer(serializers.ModelSerializer):
    """Сериализатор для модели автомобиля."""

    class Meta:
        model = Model
        fields = (
            "id",
            "name",
        )


class CarImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений автомобиля."""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CarImage
        fields = ["id", "car", "image"]


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор для модели бренда автомобиля."""

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
        )


class CarFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик автомобиля."""

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = CarFeature
        fields = ["id", "car", "name", "description"]


class CarFeatureCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления характеристик автомобиля."""

    class Meta:
        model = CarFeature
        fields = ["name"]


class CarOptionSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), required=True)

    class Meta:
        model = CarOption
        fields = ["id", "car", "name", "price"]

    def create(self, validated_data):
        """
        Метод для создания нового объекта CarOption.
        Мы извлекаем ID автомобиля из переданных данных и связываем его с создаваемым объектом.
        """
        car = validated_data.get("car")
        name = validated_data.get("name")
        price = validated_data.get("price")

        car_option = CarOption.objects.create(car=car, name=name, price=price)
        return car_option

    def update(self, instance, validated_data):
        """
        Метод для обновления существующего объекта CarOption.
        """
        instance.car = validated_data.get("car", instance.car)
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance


class CarEquipmentSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), required=True)

    class Meta:
        model = CarEquipment
        fields = ["id", "car", "name"]

    def create(self, validated_data):
        """
        Метод для создания нового объекта CarEquipment.
        Мы извлекаем ID автомобиля из переданных данных и связываем его с создаваемым объектом.
        """
        car = validated_data.get("car")
        name = validated_data.get("name")

        car_equipment = CarEquipment.objects.create(car=car, name=name)
        return car_equipment

    def update(self, instance, validated_data):
        """
        Метод для обновления существующего объекта CarEquipment.
        """
        instance.car = validated_data.get("car", instance.car)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class RentalDiscountSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения тарифного плана (скидок)."""

    class Meta:
        model = RentalDiscount
        fields = ["id", "name", "discount_week", "discount_month"]


class RentalConditionSerializer(serializers.ModelSerializer):
    """Сериализатор для условий аренды автомобиля."""

    class Meta:
        model = RentalCondition
        fields = [
            "id",
            "car",
            "insurance_deposit",
            "required_documents",
            "min_driver_age",
            "min_driving_experience",
        ]


class RentalSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = [
            "id",
            "user",
            "car",
            "pickup_datetime",
            "return_datetime",
            "return_location",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.calculate_total_price()


class CarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра автомобилей без расчета аренды.
    Реализуеться метод retrive

    """

    owner = serializers.StringRelatedField(read_only=True)
    features = CarFeatureSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    discount_policy = RentalDiscountSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    options = CarOptionSerializer(many=True, read_only=True)
    equipments = CarEquipmentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()  
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "id",
            "owner",
            "brand",
            "body_type",
            "price_per_day",
            "features",
            "images",
            "discount_policy",
            "description",
            "options",
            "equipments",
            "average_rating",
            "review_count",  
        )

    def get_average_rating(self, obj):
        """
        Возвращает средний рейтинг автомобиля.
        Использует метод get_average_rating из модели CarReview.
        """
        return CarReview.get_average_rating(obj)

    def get_review_count(self, obj):
        """
        Возвращает количество отзывов для автомобиля.
        Использует метод get_review_count из модели CarReview.
        """
        return CarReview.get_review_count(obj)


class CarListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка автомобилей.
    Оптимизирован для метода list — загружает только основные данные и первое изображение.
    """

    brand = serializers.CharField(source="brand.name", read_only=True)
    first_image = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()  
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "id",
            "brand",
            "year_of_production",
            "engine_power",
            "drive_type",
            "engine_type",
            "price_per_day",
            "first_image",
            "average_rating",
            "review_count",  
        )

    def get_first_image(self, obj):
        """
        Возвращает первое изображение автомобиля, если оно есть.
        """
        if hasattr(obj, "first_image") and obj.first_image:
            return obj.first_image[0].image.url  # Берем URL первой картинки
        return None

    def get_average_rating(self, obj):
        """
        Возвращает средний рейтинг автомобиля.
        Использует метод get_average_rating из модели CarReview.
        """
        return CarReview.get_average_rating(obj)

    def get_review_count(self, obj):
        """
        Возвращает количество отзывов для автомобиля.
        Использует метод get_review_count из модели CarReview.
        """
        return CarReview.get_review_count(obj)

class CarCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления автомобиля с указанием тарифного плана (по названию)."""

    features = CarFeatureCreateUpdateSerializer(many=True)
    discount_policy = serializers.CharField(write_only=True, required=False)
    brand_name = serializers.CharField(write_only=True)
    model_name = serializers.CharField(write_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Car
        fields = (
            "id",
            "owner",
            "brand_name",
            "model_name",
            "description",
            "body_type",
            "price_per_day",
            "year_of_production",
            "engine_power",
            "drive_type",
            "engine_type",
            "features",
            "discount_policy",
        )

    def create(self, validated_data):
        """Создаем автомобиль с характеристиками и тарифным планом по названию."""

        features_data = validated_data.pop("features", [])
        discount_policy_name = validated_data.pop("discount_policy", None)
        brand_name = validated_data.pop("brand_name")
        model_name = validated_data.pop("model_name")
        description = validated_data.pop("description", None)

        # Получаем тарифный план по названию (если передан)
        discount_policy = None
        if discount_policy_name:
            discount_policy = RentalDiscount.objects.filter(
                name=discount_policy_name
            ).first()

        # Получаем бренд по названию
        brand, _ = Brand.objects.get_or_create(name=brand_name)
        # Создаем модель, если она не существует
        model, created = Model.objects.get_or_create(name=model_name)

        # Создаем автомобиль
        car = Car.objects.create(
            **validated_data,
            discount_policy=discount_policy,
            brand=brand,
            model=model,
            description=description,  # Передаем описание при создании
        )

        # Создаем характеристики
        for feature_data in features_data:
            CarFeature.objects.create(car=car, **feature_data)

        return car

    def update(self, instance, validated_data):
        """Обновляем автомобиль и его тарифный план (по названию)."""

        features_data = validated_data.pop("features", [])
        discount_policy_name = validated_data.pop("discount_policy", None)
        brand_name = validated_data.pop("brand_name", None)
        model_name = validated_data.pop("model_name", None)
        description = validated_data.pop("description", None)

        instance.body_type = validated_data.get("body_type", instance.body_type)
        instance.price_per_day = validated_data.get(
            "price_per_day", instance.price_per_day
        )

        if discount_policy_name:
            instance.discount_policy = RentalDiscount.objects.filter(
                name=discount_policy_name
            ).first()

        if brand_name:
            brand = Brand.objects.filter(name=brand_name).first()
            if not brand:
                raise serializers.ValidationError(
                    f"Brand with name '{brand_name}' does not exist."
                )
            instance.brand = brand

        if model_name:
            model, created = Model.objects.get_or_create(
                name=model_name
            )  # Создаем или получаем модель
            instance.model = model

        if description is not None:
            instance.description = description

        instance.save()

        for feature_data in features_data:
            CarFeature.objects.update_or_create(car=instance, **feature_data)

        return instance
