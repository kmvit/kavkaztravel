from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Restaurant.
    
    Позволяет преобразовывать данные о ресторане в формат JSON и обратно. 
    Включает информацию о владельце, отзывах и рейтинге ресторана.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
   

    class Meta:
        model = Restaurant
        fields = "__all__"
