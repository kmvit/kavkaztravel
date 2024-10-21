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
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (IsOwnerOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerOnly,)


class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer


class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer


class AccommodationTypeViewSet(viewsets.ModelViewSet):
    queryset = AccommodationType.objects.all()
    serializer_class = AccommodationTypeSerializer


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
