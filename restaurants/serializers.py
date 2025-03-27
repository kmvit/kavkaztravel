from rest_framework import serializers
from .models import Restaurant, RestaurantImage, Service, RestaurantType, Region

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "description")
        extra_kwargs = {
            'name': {'validators': []}  # Отключаем автоматические валидаторы
        }

class RestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = ("id", "name", "description")
        extra_kwargs = {
            'name': {'validators': []}  # Отключаем автоматические валидаторы
        }

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
            "average_check"
        )

    def get_short_description(self, obj):
        return obj.description[:50] + '...' if obj.description else None

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
            'id',
            'name',
            'address',
            'region',
            'owner',
            'average_check',
            'description',
            'restaurant_type',
            'working_hours',
            'services',
            'images'
        ]

class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_type = RestaurantTypeSerializer()
    services = ServiceSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'region',
            'average_check', 'description', 'working_hours',
            'restaurant_type', 'services',
        ]

    def create(self, validated_data):
        # Обработка типа ресторана
        restaurant_type_data = validated_data.pop('restaurant_type')
        restaurant_type, _ = RestaurantType.objects.get_or_create(
            name=restaurant_type_data['name'],
            defaults=restaurant_type_data  # Создаем только если не существует
        )

        # Обработка услуг
        services = []
        for service_data in validated_data.pop('services'):
            service, _ = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data  # Создаем только если не существует
            )
            services.append(service)

        # Создаем ресторан
        restaurant = Restaurant.objects.create(
            restaurant_type=restaurant_type,
            **validated_data
        )
        restaurant.services.set(services)
        return restaurant

    def update(self, instance, validated_data):
        # Обновление типа ресторана
        if 'restaurant_type' in validated_data:
            type_data = validated_data.pop('restaurant_type')
            instance.restaurant_type, _ = RestaurantType.objects.get_or_create(
                name=type_data['name'],
                defaults=type_data
            )

        # Обновление услуг
        if 'services' in validated_data:
            services = []
            for service_data in validated_data.pop('services'):
                service, _ = Service.objects.get_or_create(
                    name=service_data['name'],
                    defaults=service_data
                )
                services.append(service)
            instance.services.set(services)

        # Обновление остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance