from rest_framework import serializers


from rest_framework import serializers, viewsets
from .models import (
    TourOperator, Tour, AttractionTour, ThemeTour, ParticipantTypeTour,
    FormatTour, DurationTour, SpecialOfferTour, GalleryTour, TourConditions,
    AvailableDateTour, Order
)
class TourOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperator
        fields = ['id', 'region', 'owner', 'license_number']

class AttractionTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionTour
        fields = ['id', 'name', 'description', 'region']

class ThemeTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeTour
        fields = ['id', 'name']

class ParticipantTypeTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantTypeTour
        fields = ['id', 'name']

class FormatTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormatTour
        fields = ['id', 'name']

class DurationTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = DurationTour
        fields = ['id', 'name']

class SpecialOfferTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOfferTour
        fields = ['id', 'offer_type', 'description']

class GalleryTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryTour
        fields = ['id', 'tour', 'image']

class TourConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourConditions
        fields = ['id', 'tour', 'group_size', 'children', 'meeting_point', 'booking_terms', 'organizational_details']

class AvailableDateTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDateTour
        fields = ['id', 'tour', 'start_date', 'end_date', 'is_active']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'tour', 'date', 'size', 'username', 'email', 'phone', 'owner']

class TourSerializer(serializers.ModelSerializer):
    attractions = AttractionTourSerializer(many=True, required=False)
    theme = ThemeTourSerializer(required=False)
    participant_types = ParticipantTypeTourSerializer(many=True, required=False)
    formats = FormatTourSerializer(many=True, required=False)
    duration = DurationTourSerializer(required=False)
    special_offer = SpecialOfferTourSerializer(required=False)

    class Meta:
        model = Tour
        fields = [
            'id', 'guide', 'title', 'description', 'region', 'attractions', 'price',
            'theme', 'participant_types', 'formats', 'duration', 'special_offer', 'created_at'
        ]

    def get_or_create_related_object(self, model, filter_field, filter_value, error_message):
        """
        Вспомогательный метод для получения связанного объекта.
        Если объект не найден, выбрасывает ошибку.
        """
        try:
            return model.objects.get(**{filter_field: filter_value})
        except model.DoesNotExist:
            raise serializers.ValidationError(error_message)

    def handle_many_to_many(self, instance, related_field, data, model_class):
        """
        Вспомогательный метод для обработки Many-to-Many связей.
        Очищает старые данные и добавляет новые, если они переданы.
        """
        if data is not None:
            getattr(instance, related_field).clear()
            for item_data in data:
                obj = self.get_or_create_related_object(
                    model_class,
                    'name',
                    item_data['name'],
                    f"{model_class.__name__} с таким названием не существует."
                )
                getattr(instance, related_field).add(obj)

    def create(self, validated_data):
        attractions_data = validated_data.pop('attractions', [])
        theme_data = validated_data.pop('theme', None)
        participant_types_data = validated_data.pop('participant_types', [])
        formats_data = validated_data.pop('formats', [])
        duration_data = validated_data.pop('duration', None)
        special_offer_data = validated_data.pop('special_offer', None)

        # Получаем связанные объекты, если данные предоставлены
        theme = (
            self.get_or_create_related_object(ThemeTour, 'name', theme_data['name'], "Тематика тура с таким названием не существует.")
            if theme_data else None
        )
        duration = (
            self.get_or_create_related_object(DurationTour, 'name', duration_data['name'], "Продолжительность тура с таким названием не существует.")
            if duration_data else None
        )
        special_offer = (
            self.get_or_create_related_object(SpecialOfferTour, 'offer_type', special_offer_data['offer_type'], "Спецпредложение с таким типом не существует.")
            if special_offer_data else None
        )

        # Создаем тур с основными полями
        tour = Tour.objects.create(
            **validated_data,
            theme=theme,
            duration=duration,
            special_offer=special_offer
        )

        # Обрабатываем Many-to-Many связи, если данные присутствуют
        self.handle_many_to_many(tour, 'attractions', attractions_data, AttractionTour)
        self.handle_many_to_many(tour, 'participant_types', participant_types_data, ParticipantTypeTour)
        self.handle_many_to_many(tour, 'formats', formats_data, FormatTour)

        return tour

    def update(self, instance, validated_data):
        attractions_data = validated_data.pop('attractions', None)
        theme_data = validated_data.pop('theme', None)
        participant_types_data = validated_data.pop('participant_types', None)
        formats_data = validated_data.pop('formats', None)
        duration_data = validated_data.pop('duration', None)
        special_offer_data = validated_data.pop('special_offer', None)

        # Обновляем связанные объекты, если переданы данные
        if theme_data is not None:
            instance.theme = self.get_or_create_related_object(
                ThemeTour, 'name', theme_data['name'], "Тематика тура с таким названием не существует."
            )
        if duration_data is not None:
            instance.duration = self.get_or_create_related_object(
                DurationTour, 'name', duration_data['name'], "Продолжительность тура с таким названием не существует."
            )
        if special_offer_data is not None:
            instance.special_offer = self.get_or_create_related_object(
                SpecialOfferTour, 'offer_type', special_offer_data['offer_type'], "Спецпредложение с таким типом не существует."
            )

        # Обновляем Many-to-Many связи, если данные переданы
        if attractions_data is not None:
            self.handle_many_to_many(instance, 'attractions', attractions_data, AttractionTour)
        if participant_types_data is not None:
            self.handle_many_to_many(instance, 'participant_types', participant_types_data, ParticipantTypeTour)
        if formats_data is not None:
            self.handle_many_to_many(instance, 'formats', formats_data, FormatTour)

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
