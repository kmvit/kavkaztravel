from .filter import TourFilter
from rest_framework import viewsets, permissions
from .models import DateTour, EstimationTour, GalleryTour, Geo, Guide, Order, Tag, Tour, TourOperator
from .serializers import DateTourrSerializer, EstimationTourGetSerializer, EstimationTourSerializer, GalleryTourSerializer, GeoSerializer, GuideSerializer, OrderGetSerializer, OrderSerializer, TagSerializer, TourGETSerializer, TourOperatorSerializer, TourSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TourOperatorViewSet(viewsets.ModelViewSet):
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourGETSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TourGETSerializer
        return TourSerializer

    def perform_create(self, serializer):
        """
        Переопределяем метод perform_create.

        Автоматически привязываем урок к секции и пользователю,
        сделавшему запрос.
        """
        tour_operator_id = int(self.request.data.get("tour_operator"))
        tour_operator = get_object_or_404(TourOperator, id=tour_operator_id)
        tag_id = int(self.request.data.get("tag"))
        tag = get_object_or_404(Tag, id=tag_id)
        serializer.save(tour_operator=tour_operator, tag=tag)
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Переопределяем метод perform_update.

        Автоматически привязываем урок к секции.
        """
        tour_operator_id = int(
            self.request.data.get("tour_operator", self.get_object().tour_operator_id)
        )
        tour_operator = get_object_or_404(TourOperator, id=tour_operator_id)
        tag_id = int(
            self.request.data.get("tag", self.get_object().tag_id))
        tag = get_object_or_404(Tag, id=tag_id)
        serializer.save(tour_operator=tour_operator, tag=tag)
        return Response(status=status.HTTP_200_OK)

class GalleryTourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GalleryTour.objects.all()
    serializer_class = GalleryTourSerializer

class DateTourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DateTour.objects.all()
    serializer_class = DateTourrSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class GeoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Geo.objects.all()
    serializer_class = GeoSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """Представление для управления заказами тура.
    
    Этот класс предоставляет операции для создания, чтения,
    обновления и удаления заказов, используя сериализатор OrderSerializer.
    """
    
    queryset = Order.objects.all()
   
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderGetSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        """
        Переопределяем метод perform_create.
        """
        tour_id = int(self.request.data.get("tour"))
        tour = get_object_or_404(Tour, id=tour_id)
        serializer.save(tour=tour)
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Переопределяем метод perform_update.
        """
        tour_id = int(
            self.request.data.get("tour_operator", self.get_object().tour_id)
        )
        tour = get_object_or_404(Tour, id=tour_id)
        serializer.save(tour=tour)
        return Response(status=status.HTTP_200_OK)


class EstimationTourViewSet(OrderViewSet):
    queryset = EstimationTour.objects.all()  # Получаем все объекты EstimationTour

    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EstimationTourGetSerializer
        return EstimationTourSerializer
