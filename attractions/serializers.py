from rest_framework import serializers
from .models import Attraction
from reviews.serializers import ReviewSerializer


class AttractionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для экземпляров Attraction.

    Этот сериализатор используется для преобразования данных аттрационов 
    в формат JSON и обратно. Он включает в себя информацию о рецензиях 
    и вычисляемый рейтинг аттракции.

    Атрибуты:
        reviews (ReviewSerializer): Сериализованные рецензии, связанные 
            с аттрацией. Доступны только для чтения.
        rating (float): Вычисляемый рейтинг аттракции, получаемый 
            с помощью метода get_rating.

    Метаданные:
        model (Model): Модель, для которой создается сериализатор.
        fields (list): Все поля модели, которые будут включены в 
            сериализацию.
    """
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = "__all__"

    def get_rating(self, obj):
        return obj.calculate_rating()
