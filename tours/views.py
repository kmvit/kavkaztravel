from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers, viewsets
from .models import TourOperator, Tour, TagTour, GalleryTour, AvailableDateTour, Order
from .serializers import (
    TourOperatorSerializer,
    TagTourSerializer,
    GalleryTourSerializer,
    AvailableDateTourSerializer,
    OrderSerializer,
    TourCreateUpdateSerializer,
    TourDetailSerializer,
)
from .filter import TourFilter
from .swagger_docs import (
    TourOperatorSwagger,
    GalleryTourSwagger,
    AvailableDateTourSwagger,
    OrderSwagger,
    TourSwagger,
    TagTourSwagger,
)
from .permissions import IsOwnerOrReadOnly
from .pagination import TourPagination


class GalleryTourViewSet(viewsets.ModelViewSet):
    """CRUD для Галерей туров"""

    queryset = GalleryTour.objects.all()
    serializer_class = GalleryTourSerializer
    parser_classes = [MultiPartParser, FormParser]

    @GalleryTourSwagger.gallery_tour_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @GalleryTourSwagger.gallery_tour_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @GalleryTourSwagger.gallery_tour_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @GalleryTourSwagger.gallery_tour_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @GalleryTourSwagger.gallery_tour_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AvailableDateTourViewSet(viewsets.ModelViewSet):
    """CRUD для Доступных дат туров"""

    queryset = AvailableDateTour.objects.filter(start_date__gte=timezone.now().date())
    serializer_class = AvailableDateTourSerializer

    @AvailableDateTourSwagger.available_date_tour_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @AvailableDateTourSwagger.available_date_tour_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @AvailableDateTourSwagger.available_date_tour_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @AvailableDateTourSwagger.available_date_tour_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @AvailableDateTourSwagger.available_date_tour_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD для Заказов туров"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @OrderSwagger.order_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @OrderSwagger.order_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @OrderSwagger.order_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @OrderSwagger.order_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @OrderSwagger.order_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TourViewSet(viewsets.ModelViewSet):
    """CRUD для Туров"""

    queryset = (
        Tour.objects.select_related("guide", "region")
        .prefetch_related("tags", "gallery_tour")
        .order_by("id")
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = TourPagination

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action in ["create", "update"]:
            return TourCreateUpdateSerializer
        return TourDetailSerializer

    @TourSwagger.tour_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @TourSwagger.tour_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @TourSwagger.tour_retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @TourSwagger.tour_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @TourSwagger.tour_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @TourSwagger.my_tours
    @action(detail=False, methods=["get"])
    def my_tours(self, request):
        """
        Метод для получения только туров текущего пользователя (гида).
        """
        tours = Tour.objects.filter(guide=request.user)
        page = self.paginate_queryset(tours)
        if page is not None:
            serializer = TourDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TourDetailSerializer(tours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagTourViewSet(viewsets.ModelViewSet):
    """CRUD для Тегов"""

    queryset = TagTour.objects.all()
    serializer_class = TagTourSerializer

    @TagTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @TagTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @TagTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @TagTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @TagTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TourOperatorViewSet(viewsets.ModelViewSet):
    """CRUD для Туроператоров"""

    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer

    @TourOperatorSwagger.tour_operator_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @TourOperatorSwagger.tour_operator_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @TourOperatorSwagger.tour_operator_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @TourOperatorSwagger.tour_operator_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @TourOperatorSwagger.tour_operator_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
