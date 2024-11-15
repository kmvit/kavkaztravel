from django.shortcuts import get_object_or_404
from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets, permissions

from .filters import HotelFilter
from .models import (
    Hotel,
    ReviewHotel,
    Room,
    RoomImage,
    MealPlan,
    AccommodationType,
    Amenity,
)
from .serializers import (
    HotelSerializer,
    ReviewHotelGetSerializer,
    ReviewHotelSerializer,
    RoomSerializer,
    RoomImageSerializer,
    MealPlanSerializer,
    AccommodationTypeSerializer,
    AmenitySerializer,
)
from django_filters.rest_framework import DjangoFilterBackend


class HotelViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления гостиницами.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели Hotel, включая создание, чтение, обновление и
    удаление гостиниц. Доступ к действиям ограничен только владельцам
    объектов.

    Атрибуты:
        filter_backends (list): Бэкэнды фильтрации для обработки запросов.
        filterset_class (FilterSet): Класс фильтрации для гостиниц.
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (IsOwnerOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления номерами гостиниц.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели Room, включая создание, чтение, обновление и
    удаление номеров. Доступ к действиям ограничен только владельцам
    объектов.

    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerOnly,)


class RoomImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления изображениями номеров.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели RoomImage, включая создание, чтение, обновление и
    удаление изображений номеров.
    """

    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer


class MealPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления планами питания.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели MealPlan, включая создание, чтение, обновление и
    удаление планов питания.
    """

    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer


class AccommodationTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления типами размещения.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели AccommodationType, включая создание, чтение,
    обновление и удаление типов размещения.
    """

    queryset = AccommodationType.objects.all()
    serializer_class = AccommodationTypeSerializer


class AmenityViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления удобствами.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели Amenity, включая создание, чтение, обновление и
    удаление удобств.
    """

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


class ReviewHotelViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = ReviewHotel.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewHotelGetSerializer
        return ReviewHotelSerializer

    def perform_create(self, serializer):
        """Переопределяем метод perform_create для создания нового отзыва."""

        hotel_id = self.request.data.get("hotel")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer.save(hotelr=hotel, owner=self.request.user)

    def perform_update(self, serializer):
        """Переопределяем метод perform_update для обновления отзыва."""
        # Получаем ID тура из запроса или текущего объекта
        hotel_id = self.request.data.get("hotel", self.get_object().hotel.id)

        # Используем get_object_or_404 для получения тура
        hotel = get_object_or_404(Hotel, id=hotel_id)

        # Сохраняем отзыв с обновленным туром
        serializer.save(hotel=hotel, owner=self.request.user)
