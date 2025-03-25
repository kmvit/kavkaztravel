from rest_framework import serializers
<<<<<<< Updated upstream
from .models import Restaurant
from reviews.serializers import ReviewSerializer
=======
from .models import Restaurant, RestaurantImage, Service, RestaurantType, Region
>>>>>>> Stashed changes

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "description")

class RestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = ("id", "name", "description")

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

<<<<<<< Updated upstream
    owner = serializers.ReadOnlyField(source="owner.username")
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_rating(self, obj):
        """Вычисляет и возвращает рейтинг ресторана на основе отзывов."""
        return obj.calculate_rating()
=======
class RestaurantSerializer(serializers.ModelSerializer):
    # Поля для приема JSON от фронта
    restaurant_type = serializers.DictField(
        child=serializers.CharField(),
        help_text='{"name": "Тип кухни"}'
    )
    services = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            help_text='[{"name": "Услуга"}]'
        )
    )
    # Поля для отдачи данных (GET)
    restaurant_type_info = serializers.SerializerMethodField(read_only=True)
    services_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'region',
            'average_check', 'description', 'working_hours',
            'restaurant_type', 'services',
            'restaurant_type_info', 'services_info'  
        ]
     

    def get_restaurant_type_info(self, obj):
        if obj.restaurant_type:
            return {
                'id': obj.restaurant_type.id,
                'name': obj.restaurant_type.name
            }
        return None

    def get_services_info(self, obj):
        return [
            {'id': s.id, 'name': s.name}
            for s in obj.services.all()
        ]

    def create(self, validated_data):
        # Обрабатываем тип ресторана
        restaurant_type_data = validated_data.pop('restaurant_type', None)
        if restaurant_type_data and 'name' in restaurant_type_data:
            restaurant_type, _ = RestaurantType.objects.get_or_create(
                name=restaurant_type_data['name'],
                defaults=restaurant_type_data
            )
            validated_data['restaurant_type_id'] = restaurant_type.id

        # Обрабатываем услуги
        services_data = validated_data.pop('services', [])
        service_ids = []
        for service_data in services_data:
            if 'name' in service_data:
                service, _ = Service.objects.get_or_create(
                    name=service_data['name'],
                    defaults=service_data
                )
                service_ids.append(service.id)

        # Создаем ресторан
        restaurant = Restaurant.objects.create(**validated_data)
        
        # Устанавливаем связи M2M
        if service_ids:
            restaurant.services.set(service_ids)

        return restaurant

    def update(self, instance, validated_data):
        # Обработка restaurant_type
        if 'restaurant_type' in validated_data:
            rt_data = validated_data.pop('restaurant_type')
            instance.restaurant_type = RestaurantType.objects.get_or_create(
                name=rt_data['name']  # Ищем ТОЛЬКО по name, другие поля не обновляем
            )[0]  # Берём первый элемент (объект, не созданный)

        # Обработка services
        if 'services' in validated_data:
            services = []
            for service_data in validated_data.pop('services'):
                service = Service.objects.get_or_create(
                    name=service_data['name']  # Только проверка по name
                )[0]  # Существующий или новый (без обновления)
                services.append(service)
            instance.services.set(services)  # Полная замена связей

        # Обновляем основные поля ресторана
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
>>>>>>> Stashed changes
