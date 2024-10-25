from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.

    Этот сериализатор преобразует объекты Review в формат JSON и обратно.
    Он позволяет валидировать данные, получаемые от клиента, и обеспечивает
    необходимое представление отзывов.

    """

    class Meta:
        model = Review
        fields = "__all__"
