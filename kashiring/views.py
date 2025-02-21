from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Brand, Model, Year, Color, BodyType, Auto, Foto, Company
from .serializers import (
    BrandSerializer,
    ModelSerializer,
    YearSerializer,
    ColorSerializer,
    BodyTypeSerializer,
    AutoSerializer,
    AutoGETSerializer,
    CompanyAutoSerializer,
    CompanySerializer,
)
from django.shortcuts import get_object_or_404
from http import HTTPStatus
from rest_framework import status
from rest_framework.response import Response


class CarViewSet(viewsets.ModelViewSet):
    """ViewSet для управления автомобилями, включая условия аренды."""
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.prefetch_related('rental_condition')


class CarImageViewSet(viewsets.ModelViewSet):
    """ViewSet для добавления и удаления фотографий автомобилей."""
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer


class RentalConditionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления условиями аренды автомобилей."""
    queryset = RentalCondition.objects.all()
    serializer_class = RentalConditionSerializer
