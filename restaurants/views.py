from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .filters import RestaurantFilter
from .models import Restaurant, RestaurantImage
from .pagination import ReviewPagination
from .serializers import (
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    RestaurantImageSerializer,
    RestaurantSerializer,
)
from .swagger_docs import (
    restaurant_create,
    restaurant_list,
    restaurant_detail,
    restaurant_update,
    restaurant_delete,
    restaurant_image_upload,
    restaurant_image_update,
    restaurant_image_delete,
)
from kashiring.permissions import IsOwnerOrReadOnly


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления основными данными ресторанов.

    Этот ViewSet предоставляет CRUD операции для ресторанов, а также фильтрацию,
    пагинацию и выбор нужного сериализатора в зависимости от действия.
    """

    queryset = Restaurant.objects.select_related(
        "region", "restaurant_type"
    ).prefetch_related("services", "images")
    serializer_class = RestaurantDetailSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RestaurantFilter
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ReviewPagination

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantListSerializer
        elif self.action == "retrieve":
            return RestaurantDetailSerializer
        return RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @restaurant_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @restaurant_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @restaurant_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @restaurant_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @restaurant_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RestaurantImageViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet для управления изображениями ресторанов.
    Поддерживает только создание, обновление и удаление.
    """

    serializer_class = RestaurantImageSerializer
    queryset = RestaurantImage.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @restaurant_image_upload
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @restaurant_image_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @restaurant_image_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
