from Kavkaztome.permissions import IsOwnerOnly

from .filter import TourFilter
from rest_framework import viewsets
from rest_framework import serializers, viewsets
from .models import (
    TourOperator, Tour, Tag, GalleryTour,
    AvailableDateTour, Order
)
from .serializers import (
    TourOperatorSerializer,
    TagSerializer,
    GalleryTourSerializer,
    AvailableDateTourSerializer,
    OrderSerializer,
    TourCreateUpdateSerializer,
    TourDetailSerializer
)
from .swagger_docs import (
    TourOperatorSwagger,
    GalleryTourSwagger,
    AvailableDateTourSwagger,
    OrderSwagger,
    TourSwagger,
    TagSwagger
)




class GalleryTourViewSet(viewsets.ModelViewSet):
    """CRUD для Галерей туров"""
    queryset = GalleryTour.objects.all()
    serializer_class = GalleryTourSerializer

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
    queryset = AvailableDateTour.objects.all()
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

    @OrderSwagger. order_detail
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
    queryset = Tour.objects.select_related(
        'guide', 'region'
    ).prefetch_related(
        'tags',
        'gallery_tour'  # Добавляем prefetch для галереи
    )
    
    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action in ['create', 'update']:
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


  # или откуда импортируешь

class TagViewSet(viewsets.ModelViewSet):
    """CRUD для Тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @TagSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @TagSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @TagSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @TagSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @TagSwagger.destroy
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