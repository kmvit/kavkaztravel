from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from Kavkaztome.permissions import IsOwnerOnly
from .models import (
    Brand,
    Model,
    ReviewAuto,
    ReviewImageAuto,
    Year,
    Color,
    BodyType,
    Auto,
    Company,
)
from .serializers import (
    BrandSerializer,
    ModelSerializer,
    ReviewAutoSerializer,
    YearSerializer,
    ColorSerializer,
    BodyTypeSerializer,
    AutoSerializer,
    AutoGETSerializer,
    CompanyAutoSerializer,
    CompanySerializer,
)


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
    parser_classes = (MultiPartParser, FormParser)  # Для обработки изображений
    serializer_class = ReviewAutoSerializer

    def create(self, request, *args, **kwargs):
        # Создание отзыва
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем отзыв
            review = serializer.save()

            # Если есть изображения, сохраняем их
            review_images = request.FILES.getlist('review_images')
            if review_images:
                for image in review_images:
                    ReviewImageAuto.objects.create(review=review, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # Получаем отзыв для обновления
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Обновление отзыва
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            # Сохраняем обновленный отзыв
            review = serializer.save()

            # Обработка изображений:
            review_images = request.FILES.getlist('review_images')
            if review_images:
                # Удаляем старые изображения
                review.review_images.all().delete()

                # Добавляем новые изображения
                for image in review_images:
                    ReviewImageAuto.objects.create(review=review, image=image)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
