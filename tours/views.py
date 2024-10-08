from rest_framework import viewsets, permissions
from .models import DateTour, GalleryTour, Guide, Tag, Tour, TourOperator
from .serializers import DateTourrSerializer, GalleryTourSerializer, GuideSerializer, TourGETSerializer, TourOperatorSerializer, TourSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

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