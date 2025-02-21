# Сериализаторы
class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CarFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор для характеристик автомобиля."""
    class Meta:
        model = CarFeature
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для автомобилей, включая характеристики и условия аренды."""
    features = CarFeatureSerializer(many=True, read_only=True)
    rental_condition = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Car
        fields = '__all__'

class CarImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений автомобиля."""
    class Meta:
        model = CarImage
        fields = '__all__'

class RentalConditionSerializer(serializers.ModelSerializer):
    """Сериализатор для условий аренды автомобиля."""
    class Meta:
        model = RentalCondition
        fields = '__all__'
