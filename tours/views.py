from Kavkaztome.permissions import IsOwnerOnly

from .filter import TourFilter
from rest_framework import viewsets
from rest_framework import serializers, viewsets
from .models import (
    TourOperator, Tour, AttractionTour, ThemeTour, ParticipantTypeTour,
    FormatTour, DurationTour, SpecialOfferTour, GalleryTour,
    AvailableDateTour, Order
)
from .serializers import (
    TourOperatorSerializer,
    AttractionTourSerializer,
    ThemeTourSerializer,
    ParticipantTypeTourSerializer,
    FormatTourSerializer,
    DurationTourSerializer,
    SpecialOfferTourSerializer,
    GalleryTourSerializer,
    AvailableDateTourSerializer,
    OrderSerializer,
    TourSerializer
)
from .swagger_docs import (
    TourOperatorSwagger,
    AttractionTourSwagger,
    ParticipantTypeTourSwagger,
    FormatTourSwagger,
    DurationTourSwagger,
    SpecialOfferTourSwagger,
    GalleryTourSwagger,
    AvailableDateTourSwagger,
    OrderSwagger,
    TourSwagger,
    ThemeTourSwagger
)




class TourOperatorViewSet(viewsets.ModelViewSet):
    """CRUD для Туроператоров"""
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer

    @TourOperatorSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @TourOperatorSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @TourOperatorSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @TourOperatorSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @TourOperatorSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class AttractionTourViewSet(viewsets.ModelViewSet):
    """CRUD для Достопримечательностей туров"""
    queryset = AttractionTour.objects.all()
    serializer_class = AttractionTourSerializer

    @AttractionTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @AttractionTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @AttractionTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @AttractionTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @AttractionTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ThemeTourViewSet(viewsets.ModelViewSet):
    """ CRUD для Тем туров """
    queryset = ThemeTour.objects.all()
    serializer_class = ThemeTourSerializer

    @ThemeTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @ThemeTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @ThemeTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @ThemeTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @ThemeTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class ParticipantTypeTourViewSet(viewsets.ModelViewSet):
    """CRUD для Типов участников туров"""
    queryset = ParticipantTypeTour.objects.all()
    serializer_class = ParticipantTypeTourSerializer

    @ParticipantTypeTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @ParticipantTypeTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @ParticipantTypeTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @ParticipantTypeTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @ParticipantTypeTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class FormatTourViewSet(viewsets.ModelViewSet):
    """CRUD для Форматов туров"""
    queryset = FormatTour.objects.all()
    serializer_class = FormatTourSerializer

    @FormatTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @FormatTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @FormatTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @FormatTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @FormatTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class DurationTourViewSet(viewsets.ModelViewSet):
    """CRUD для Продолжительности туров"""
    queryset = DurationTour.objects.all()
    serializer_class = DurationTourSerializer

    @DurationTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @DurationTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @DurationTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @DurationTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @DurationTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class SpecialOfferTourViewSet(viewsets.ModelViewSet):
    """CRUD для Спецпредложений туров"""
    queryset = SpecialOfferTour.objects.all()
    serializer_class = SpecialOfferTourSerializer

    @SpecialOfferTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @SpecialOfferTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @SpecialOfferTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @SpecialOfferTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @SpecialOfferTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class GalleryTourViewSet(viewsets.ModelViewSet):
    """CRUD для Галерей туров"""
    queryset = GalleryTour.objects.all()
    serializer_class = GalleryTourSerializer

    @GalleryTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @GalleryTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @GalleryTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @GalleryTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @GalleryTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AvailableDateTourViewSet(viewsets.ModelViewSet):
    """CRUD для Доступных дат туров"""
    queryset = AvailableDateTour.objects.all()
    serializer_class = AvailableDateTourSerializer

    @AvailableDateTourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @AvailableDateTourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @AvailableDateTourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @AvailableDateTourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @AvailableDateTourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class OrderViewSet(viewsets.ModelViewSet):
    """CRUD для Заказов туров"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @OrderSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @OrderSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @OrderSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @OrderSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @OrderSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class TourViewSet(viewsets.ModelViewSet):
    """CRUD для Туров"""
    queryset = Tour.objects.select_related(
        'guide', 'region', 'theme', 'duration', 'special_offer'
    ).prefetch_related(
        'attractions', 'participant_types', 'formats'
    )
    serializer_class = TourSerializer

    @TourSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @TourSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @TourSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @TourSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @TourSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)