from rest_framework import serializers
from .models import Restaurant, RestaurantImage, Service, RestaurantType, Region
from django.db import transaction


class RestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = ("id", "name", "description")
        extra_kwargs = {"name": {"validators": []}}

    def validate_name(self, value):
        return value


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "description")
        extra_kwargs = {"name": {"validators": []}}

    def validate_name(self, value):
        return value


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ("id", "image", "restaurant")


class RestaurantListSerializer(serializers.ModelSerializer):
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
        return obj.description[:50] + "..." if obj.description else None

    def get_main_image(self, obj):
        image = obj.images.first()
        return image.image.url if image else None


class RestaurantDetailSerializer(serializers.ModelSerializer):
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
        # Нормализуем имя вручную, на случай если to_internal_value не сработало
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
        with transaction.atomic():
            restaurant_type_data = validated_data.pop("restaurant_type")
            # Передаем restaurant_type_data через наш сериалайзер, чтобы to_internal_value нормализовал данные
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
