from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Brand, Model, ReviewAuto, Year, Color, BodyType, Auto, Company
from .serializers import (
    BrandSerializer,
    ModelSerializer,
    ReviewAutoGetSerializer,
    ReviewAutoSerializer,
    YearSerializer,
    ColorSerializer,
    BodyTypeSerializer,
    AutoSerializer,
    AutoGETSerializer,
    CompanyAutoSerializer,
    CompanySerializer,
)
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response


class BrandViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Brand.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ModelViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Model.
    """

    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class YearViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Year.
    """

    queryset = Year.objects.all()
    serializer_class = YearSerializer


class ColorViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Color.
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class BodyTypeViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями BodyType.
    """

    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer


class AutoViewSet(viewsets.ModelViewSet):
    """
    Представление для CRUD операций с моделями Auto.
    """

    queryset = Auto.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        """Функция выбора класса - сериализатора в зависимости от метода"""
        if self.action in ("list", "retrieve"):
            return AutoGETSerializer
        return AutoSerializer

    def perform_create(self, serializer):
        brand_id = int(self.request.data.get("brand"))
        brand = get_object_or_404(Brand, id=brand_id)
        model_id = int(self.request.data.get("model"))
        model = get_object_or_404(Model, id=model_id)
        year_id = self.request.data.get("year")
        year = get_object_or_404(Year, id=year_id)
        color_id = int(self.request.data.get("color"))
        color = get_object_or_404(Color, id=color_id)
        body_type_id = int(self.request.data.get("body_type"))
        body_type = get_object_or_404(BodyType, id=body_type_id)

        serializer.save(
            brand=brand,
            model=model,
            color=color,
            year=year,
            body_type=body_type,
            owner=self.request.user,
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        brand_id = int(self.request.data.get("brand", self.get_object().brand.id))
        brand = get_object_or_404(Brand, id=brand_id)
        model_id = int(self.request.data.get("model", self.get_object().model.id))
        model = get_object_or_404(Model, id=model_id)
        year_id = self.request.data.get("year", self.get_object().year.id)
        year = get_object_or_404(Year, id=year_id)
        color_id = int(self.request.data.get("color", self.get_object().color.id))
        color = get_object_or_404(Color, id=color_id)
        body_type_id = int(
            self.request.data.get("body_type", self.get_object().body_type.id)
        )
        body_type = get_object_or_404(BodyType, id=body_type_id)

        serializer.save(
            brand=brand,
            model=model,
            color=color,
            year=year,
            body_type=body_type,
            owner=self.request.user,
        )
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


class CompanyAutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для READ операций с моделями Company и получения машины.
    """

    queryset = Company.objects.all()
    serializer_class = CompanyAutoSerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для READ операций с моделями Company.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ReviewAutoViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = ReviewAuto.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewAutoGetSerializer
        return ReviewAutoSerializer

    def perform_create(self, serializer):
        """Переопределяем метод perform_create для создания нового отзыва."""

        auto_id = self.request.data.get("auto")
        restaurant = get_object_or_404(Auto, id=auto_id)
        serializer.save(tour=restaurant, owner=self.request.user)

    def perform_update(self, serializer):
        """Переопределяем метод perform_update для обновления отзыва."""
        # Получаем ID тура из запроса или текущего объекта
        auto_id = self.request.data.get("auto", self.get_object().auto.id)

        # Используем get_object_or_404 для получения тура
        auto = get_object_or_404(Auto, id=auto_id)

        # Сохраняем отзыв с обновленным туром
        serializer.save(auto=auto, owner=self.request.user)
