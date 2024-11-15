from Kavkaztome.permissions import IsOwnerOnly

from .filter import TourFilter
from rest_framework import viewsets
from .models import (
    DateTour,
    ReviewTour,
    GalleryTour,
    Geo,
    Guide,
    Order,
    Tag,
    Tour,
    TourOperator,
)
from .serializers import (
    DateTourrSerializer,
    GalleryTourSerializer,
    GeoSerializer,
    GuideSerializer,
    OrderGetSerializer,
    OrderSerializer,
    ReviewTourGetSerializer,
    ReviewTourSerializer,
    TagSerializer,
    TourGETSerializer,
    TourOperatorSerializer,
    TourSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class GuideViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления объектами модели Guide.

    Предоставляет полный набор действий (CRUD) для работы с гидами.
    """

    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = (IsOwnerOnly,)


class TourOperatorViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления объектами модели TourOperator.

    Предоставляет полный набор действий (CRUD) для работы с туроператорами.
    """

    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer
    permission_classes = (IsOwnerOnly,)


class TourViewSet(viewsets.ModelViewSet):
    """Представление для управления тура.

    Этот класс предоставляет операции для создания, чтения,
    обновления и удаления заказов.
    Также представление делать выборку из таблицы по тэгам,
    геолокациям, и тэгам и геолакациям.
    """

    queryset = Tour.objects.all()
    serializer_class = TourGETSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        "Функция выбора сериализатора в зависимости от метода."
        if self.action in ("list", "retrieve"):
            return TourGETSerializer
        return TourSerializer

    def perform_create(self, serializer):
        """
        Переопределяем метод perform_create.
        """
        tour_operator_id = int(self.request.data.get("tour_operator"))
        tour_operator = get_object_or_404(TourOperator, id=tour_operator_id)
        tag_id = int(self.request.data.get("tag"))
        tag = get_object_or_404(Tag, id=tag_id)
        geo_id = int(self.request.data.get("geo"))
        geo = get_object_or_404(Geo, id=geo_id)
        serializer.save(
            tour_operator=tour_operator, tag=tag, geo=geo, owner=self.request.user
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Переопределяем метод perform_update.
        """
        tour_operator_id = int(
            self.request.data.get("tour_operator", self.get_object().tour_operator_id)
        )
        tour_operator = get_object_or_404(TourOperator, id=tour_operator_id)
        tag_id = int(self.request.data.get("tag", self.get_object().tag_id))
        tag = get_object_or_404(Tag, id=tag_id)
        geo_id = int(self.request.data.get("geo", self.get_object().geo_id))
        geo = get_object_or_404(Geo, id=geo_id)
        serializer.save(
            tour_operator=tour_operator, tag=tag, geo=geo, owner=self.request.user
        )
        return Response(status=status.HTTP_200_OK)


class GalleryTourViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот класс предоставляет операции для чтения
    изображения тура.
    """

    queryset = GalleryTour.objects.all()
    serializer_class = GalleryTourSerializer


class DateTourViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот класс предоставляет операции для чтения
    дат и продолжительности тура.
    """

    queryset = DateTour.objects.all()
    serializer_class = DateTourrSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот класс предоставляет операции для чтения
    тэгов тура.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class GeoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот класс предоставляет операции для чтения
    геолокаций тура.
    """

    queryset = Geo.objects.all()
    serializer_class = GeoSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Представление для управления заказами тура.

    Этот класс предоставляет операции для создания, чтения,
    обновления и удаления заказов, используя сериализатор OrderSerializer.
    """

    queryset = Order.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderGetSerializer
        return OrderSerializer


class ReviewTourViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = ReviewTour.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewTourGetSerializer
        return ReviewTourSerializer

    def perform_create(self, serializer):
        """Переопределяем метод perform_create для создания нового отзыва."""

        tour_id = self.request.data.get("tour")
        tour = get_object_or_404(Tour, id=tour_id)
        serializer.save(tour=tour, owner=self.request.user)

    def perform_update(self, serializer):
        """Переопределяем метод perform_update для обновления отзыва."""
        # Получаем ID тура из запроса или текущего объекта
        tour_id = self.request.data.get("tour", self.get_object().tour.id)

        # Используем get_object_or_404 для получения тура
        tour = get_object_or_404(Tour, id=tour_id)

        # Сохраняем отзыв с обновленным туром
        serializer.save(tour=tour, owner=self.request.user)
