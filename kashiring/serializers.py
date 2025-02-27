from rest_framework import serializers
from .models import Car, CarFeature, RentalCondition, CarImage, Rental, RentalDiscount


class CarImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений автомобиля."""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CarImage
        fields = ["id", "car", "image"]


class CarFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик автомобиля."""

    class Meta:
        model = CarFeature
        fields = ["id", "car", "name"]


class RentalDiscountSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения тарифного плана (скидок)."""

    class Meta:
        model = RentalDiscount
        fields = ["name", "discount_week", "discount_month"]


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


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра автомобилей без расчета аренды."""

    owner = serializers.StringRelatedField(read_only=True)
    features = CarFeatureSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    discount_policy = RentalDiscountSerializer(read_only=True)

    class Meta:
        model = Car
        fields = [
            "id",
            "owner",
            "brand",
            "body_type",
            "price_per_day",
            "features",
            "images",
            "discount_policy",
        ]


class CarFeatureCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления характеристик автомобиля."""

    class Meta:
        model = CarFeature
        fields = ["name"]


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления автомобиля с указанием тарифного плана (по названию)."""

    features = CarFeatureCreateUpdateSerializer(many=True)
    discount_policy = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Car
        fields = [
            "id",
            "owner",
            "brand",
            "body_type",
            "price_per_day",
            "features",
            "discount_policy",  # Поле для передачи названия тарифного плана
        ]

    def create(self, validated_data):
        """Создаем автомобиль с характеристиками и тарифным планом по названию."""

        features_data = validated_data.pop("features", [])
        discount_policy_name = validated_data.pop("discount_policy", None)

        # Получаем тарифный план по названию (если передан)
        discount_policy = None
        if discount_policy_name:
            discount_policy = RentalDiscount.objects.filter(
                name=discount_policy_name
            ).first()

        # Создаем автомобиль
        car = Car.objects.create(**validated_data, discount_policy=discount_policy)

        # Создаем характеристики
        for feature_data in features_data:
            CarFeature.objects.create(car=car, **feature_data)

        return car

    def update(self, instance, validated_data):
        """Обновляем автомобиль и его тарифный план (по названию)."""

        features_data = validated_data.pop("features", [])
        discount_policy_name = validated_data.pop("discount_policy", None)

        # Обновляем автомобиль
        instance.brand = validated_data.get("brand", instance.brand)
        instance.body_type = validated_data.get("body_type", instance.body_type)
        instance.price_per_day = validated_data.get(
            "price_per_day", instance.price_per_day
        )

        # Обновляем тарифный план (если передан)
        if discount_policy_name:
            instance.discount_policy = RentalDiscount.objects.filter(
                name=discount_policy_name
            ).first()

        instance.save()

        # Обновляем характеристики
        for feature_data in features_data:
            CarFeature.objects.update_or_create(car=instance, **feature_data)

        return instance


class RentalDiscountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RentalDiscount.

    Этот сериализатор используется для конвертации данных модели скидок
    в формат JSON и обратно. Он позволяет получать список скидок, создавать
    новые, редактировать существующие и удалять их через API.

    """

    class Meta:
        model = RentalDiscount
        fields = ["id", "name", "discount_week", "discount_month"]


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
            "daily_price",
        ]

    def get_total_price(self, obj):
        return obj.calculate_total_price_with_discount()
