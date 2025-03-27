from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Restaurant, RestaurantImage
from .serializers import (
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    RestaurantImageSerializer,
    RestaurantSerializer
)
from .swagger_docs import *
from Kavkaztome.permissions import IsOwnerOnly
from .filters import RestaurantFilter
from django_filters import rest_framework as filters
from kashiring.permissions import IsOwnerOrReadOnly
from .pagination import ReviewPagination
class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления основными данными ресторанов
    """
    queryset = Restaurant.objects.select_related("region", "restaurant_type").prefetch_related("services", "images")
    permission_classes = (IsOwnerOnly,)
    serializer_class = RestaurantDetailSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RestaurantFilter
    #permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ReviewPagination
    

    def get_serializer_class(self):
        if self.action == 'list':
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
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @restaurant_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @restaurant_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import RestaurantImage
from .serializers import RestaurantImageSerializer
from .swagger_docs import (
    restaurant_image_upload,
    restaurant_image_update,
    restaurant_image_delete
)

class RestaurantImageViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для управления изображениями ресторанов
    Поддерживает только создание, обновление и удаление
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
   