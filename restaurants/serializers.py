from rest_framework import serializers
from .models import Restaurant, RestaurantImage, Service, RestaurantType, Region
from django.db import transaction, IntegrityError


class RestaurantTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RestaurantType.

    Используется для преобразования данных типов ресторанов в JSON-формат и обратно.
    """

    class Meta:
        model = RestaurantType
        fields = ("id", "name", "description")
        extra_kwargs = {"name": {"validators": []}}

    def validate_name(self, value):
        """
        Валидатор для поля name.

        В данном случае метод просто возвращает значение без изменений.
        """
        return value


class ServiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Service.

    Преобразует данные услуг ресторана в JSON-формат и обеспечивает их валидацию.
    """

    class Meta:
        model = Service
        fields = ("id", "name", "description")
        extra_kwargs = {"name": {"validators": []}}

    def validate_name(self, value):
        """
        Валидатор для поля name.

        Возвращает значение без модификаций.
        """
        return value


class RestaurantImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RestaurantImage.

    Используется для преобразования данных изображений ресторана.
    """

    class Meta:
        model = RestaurantImage
        fields = ("id", "image", "restaurant")


class RestaurantListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления списка ресторанов.

    Отображает основные поля ресторана, включая связанные объекты: регион,
    тип ресторана, услуги и основное изображение.
    """

    region = serializers.StringRelatedField()
    restaurant_type = RestaurantTypeSerializer()
    services = ServiceSerializer(many=True)
    main_image = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "region",
            "short_description",
            "restaurant_type",
            "services",
            "main_image",
            "average_check",
        )

    def get_short_description(self, obj):
        """
        Возвращает укороченное описание ресторана.

        Если описание существует, возвращается первые 50 символов с многоточием.
        Если описания нет, возвращается None.
        """
        return obj.description[:50] + "..." if obj.description else None

    def get_main_image(self, obj):
        """
        Возвращает URL основного изображения ресторана.

        Выбирается первое изображение из связанных объектов.
        Если изображений нет, возвращается None.
        """
        image = obj.images.first()
        return image.image.url if image else None


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального представления ресторана.

    Включает подробную информацию о ресторане, а также данные о владельце,
    регионе, типе ресторана, услугах и связанных изображениях.
    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    restaurant_type = RestaurantTypeSerializer(allow_null=True, required=False)
    services = ServiceSerializer(many=True, required=False)
    images = RestaurantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "address",
            "region",
            "owner",
            "average_check",
            "description",
            "restaurant_type",
            "working_hours",
            "services",
            "images",
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления ресторанов.

    Обеспечивает корректную обработку связанных объектов, таких как тип ресторана и услуги,
    и поддерживает атомарное создание и обновление через транзакции.
    """

    restaurant_type = RestaurantTypeSerializer()
    services = ServiceSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "address",
            "region",
            "average_check",
            "description",
            "working_hours",
            "restaurant_type",
            "services",
        ]

    def handle_related_object(self, model, data):
        """
        Обрабатывает связанные объекты (например, RestaurantType или Service).

        Метод нормализует имя объекта, ищет существующую запись по имени и,
        при необходимости, обновляет описание. Если объект не найден, создаёт новый.
        """
        norm_name = data.get("name", "").strip()
        data["name"] = norm_name
        obj = model.objects.filter(name=norm_name).first()
        if obj:
            # Если передано описание и оно отличается, обновляем его
            if data.get("description") is not None and obj.description != data.get(
                "description", ""
            ):
                obj.description = data.get("description", "")
                obj.save()
            return obj
        try:
            return model.objects.create(**data)
        except IntegrityError:
            return model.objects.get(name=norm_name)

    def create(self, validated_data):
        """
        Создает новый объект Restaurant.

        Метод обрабатывает связанные данные для типа ресторана и услуг, используя
        атомарную транзакцию для обеспечения целостности данных.
        """
        with transaction.atomic():
            restaurant_type_data = validated_data.pop("restaurant_type")
            # Обработка данных типа ресторана через handle_related_object
            restaurant_type = self.handle_related_object(
                RestaurantType, restaurant_type_data
            )

            services_data = validated_data.pop("services", [])
            services = [self.handle_related_object(Service, s) for s in services_data]

            restaurant = Restaurant.objects.create(
                restaurant_type=restaurant_type, **validated_data
            )
            restaurant.services.set(services)
            return restaurant

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект Restaurant.

        Метод обновляет связанные объекты (тип ресторана и услуги) при наличии в данных,
        а затем обновляет остальные поля ресторана. Обновление происходит в рамках транзакции.
        """
        with transaction.atomic():
            if "restaurant_type" in validated_data:
                type_data = validated_data.pop("restaurant_type")
                instance.restaurant_type = self.handle_related_object(
                    RestaurantType, type_data
                )

            if "services" in validated_data:
                services_data = validated_data.pop("services", [])
                instance.services.set(
                    [self.handle_related_object(Service, s) for s in services_data]
                )

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance
