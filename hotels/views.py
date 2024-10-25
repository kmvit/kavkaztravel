from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets, permissions

from .filters import HotelFilter
from .models import Hotel, Room, RoomImage, MealPlan, AccommodationType, Amenity
from .serializers import (
    HotelSerializer,
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
