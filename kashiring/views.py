from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Car, CarImage, RentalCondition
from .serializers import CarSerializer, CarImageSerializer, RentalConditionSerializer
from .filters import CarFilter, RentalConditionFilter
from .swagger_docs import CarSwagger, CarImageSwagger, RentalConditionSwagger


class CarViewSet(viewsets.ModelViewSet):
    """API для управления автомобилями."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter


    @CarSwagger.car_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CarSwagger.car_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CarSwagger.car_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CarSwagger.car_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @CarSwagger.car_update
    def partial_update(self, request, *args, **kwargs): 
        return super().partial_update(request, *args, **kwargs)

    @CarSwagger.car_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CarImageViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """API для управления изображениями автомобилей."""

    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    parser_classes = [MultiPartParser, FormParser] 


    @CarImageSwagger.image_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CarImageSwagger.image_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CarImageSwagger.image_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CarImageSwagger.image_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RentalConditionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                             mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """API для управления условиями аренды автомобилей."""

    queryset = RentalCondition.objects.all()
    serializer_class = RentalConditionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RentalConditionFilter


    @RentalConditionSwagger.rental_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @RentalConditionSwagger.rental_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @RentalConditionSwagger.rental_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @RentalConditionSwagger.rental_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @RentalConditionSwagger.rental_update
    def partial_update(self, request, *args, **kwargs):  # ✅ PATCH метод
        return super().partial_update(request, *args, **kwargs)