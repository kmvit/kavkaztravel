from rest_framework import serializers
from .models import Car, CarFeature, CarImage, RentalDiscount,  Rental, RentalDiscount, RentalCondition, Brand, CarOption, CarEquipment


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
        fields = ("id", "name",)

class CarFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик автомобиля."""

    # Поле для необязательного описания
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
    """
    Сериализатор для дополнительной опции автомобиля.
    """
    car = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.DecimalField(required=False, allow_null=True, max_digits=10,
        decimal_places=2)

    class Meta:
        model = CarOption
        fields = ['id', 'car', 'name', 'price']

class CarEquipmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комплектации автомобиля.
    """
    car = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CarEquipment
        fields = ['id', 'car', 'name']




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
            "daily_price",
        ]

    def get_total_price(self, obj):
        return obj.calculate_total_price_with_discount()


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
        )


class CarListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка автомобилей.
    Оптимизирован для метода list — загружает только основные данные и первое изображение.
    """

    brand = serializers.CharField(source="brand.name", read_only=True)
    first_image = serializers.SerializerMethodField()

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
        )

    def get_first_image(self, obj):
        """
        Возвращает первое изображение автомобиля, если оно есть.
        """
        if hasattr(obj, "first_image") and obj.first_image:
            return obj.first_image[0].image.url  # Берем URL первой картинки
        return None


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления автомобиля с указанием тарифного плана (по названию)."""

    features = CarFeatureCreateUpdateSerializer(many=True)
    discount_policy = serializers.CharField(write_only=True, required=False)
    brand_name = serializers.CharField(write_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Car
        fields = (
            "id",
            "owner",
            "brand_name",  
            "body_type",
            "price_per_day",
            "features",
            "discount_policy",
            "description",
        )

    def create(self, validated_data):
        """Создаем автомобиль с характеристиками и тарифным планом по названию."""

        features_data = validated_data.pop("features", [])
        discount_policy_name = validated_data.pop("discount_policy", None)
        brand_name = validated_data.pop("brand_name")  # Получаем название бренда
        description = validated_data.pop("description", None)  # Получаем описание

        # Получаем тарифный план по названию (если передан)
        discount_policy = None
        if discount_policy_name:
            discount_policy = RentalDiscount.objects.filter(
                name=discount_policy_name
            ).first()

        # Получаем бренд по названию
        brand = Brand.objects.filter(name=brand_name).first()
        if not brand:
            raise serializers.ValidationError(f"Brand with name '{brand_name}' does not exist.")

        # Создаем автомобиль
        car = Car.objects.create(
            **validated_data,
            discount_policy=discount_policy,
            brand=brand,
            description=description  # Передаем описание при создании
        )

        # Создаем характеристики
        for feature_data in features_data:
            CarFeature.objects.create(car=car, **feature_data)

        return car

    def update(self, instance, validated_data):
        """Обновляем автомобиль и его тарифный план (по названию)."""

        features_data = validated_data.pop("features", [])
        discount_policy_name = validated_data.pop("discount_policy", None)
        brand_name = validated_data.pop("brand_name", None)  # Получаем название бренда
        description = validated_data.pop("description", None)  # Получаем описание

        # Обновляем автомобиль
        instance.body_type = validated_data.get("body_type", instance.body_type)
        instance.price_per_day = validated_data.get(
            "price_per_day", instance.price_per_day
        )

        # Обновляем тарифный план (если передан)
        if discount_policy_name:
            instance.discount_policy = RentalDiscount.objects.filter(
                name=discount_policy_name
            ).first()

        # Обновляем бренд, если передан новый
        if brand_name:
            brand = Brand.objects.filter(name=brand_name).first()
            if not brand:
                raise serializers.ValidationError(f"Brand with name '{brand_name}' does not exist.")
            instance.brand = brand

        # Обновляем описание, если передано новое
        if description is not None:
            instance.description = description

        instance.save()

        # Обновляем характеристики
        for feature_data in features_data:
            CarFeature.objects.update_or_create(car=instance, **feature_data)

        return instance