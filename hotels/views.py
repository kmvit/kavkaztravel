from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from Kavkaztome.permissions import IsOwnerOnly
from .filters import HotelFilter
from .models import (
    Hotel,
    ReviewHotel,
    ReviewImageHotel,
    Room,
    RoomImage,
    MealPlan,
    AccommodationType,
    Amenity,
)
from .serializers import (
    HotelSerializer,
    ReviewHotelSerializer,
    RoomSerializer,
    RoomImageSerializer,
    MealPlanSerializer,
    AccommodationTypeSerializer,
    AmenitySerializer,
)


class HotelViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления гостиницами.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели Hotel, включая создание, чтение, обновление и
    удаление гостиниц. Доступ к действиям ограничен только владельцам
    объектов.

    Атрибуты:
        filter_backends (list): Бэкэнды фильтрации для обработки запросов.
        filterset_class (FilterSet): Класс фильтрации для гостиниц.
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (IsOwnerOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления номерами гостиниц.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели Room, включая создание, чтение, обновление и
    удаление номеров. Доступ к действиям ограничен только владельцам
    объектов.

    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerOnly,)


class RoomImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления изображениями номеров.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели RoomImage, включая создание, чтение, обновление и
    удаление изображений номеров.
    """

    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer


class MealPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления планами питания.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели MealPlan, включая создание, чтение, обновление и
    удаление планов питания.
    """

    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer


class AccommodationTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления типами размещения.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели AccommodationType, включая создание, чтение,
    обновление и удаление типов размещения.
    """

    queryset = AccommodationType.objects.all()
    serializer_class = AccommodationTypeSerializer


class AmenityViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления удобствами.

    Этот ViewSet предоставляет полный набор действий для работы с
    объектами модели Amenity, включая создание, чтение, обновление и
    удаление удобств.
    """

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
# views.py


class ReviewHotelViewSet(viewsets.ModelViewSet):
    queryset = ReviewHotel.objects.all()
    serializer_class = ReviewHotelSerializer
    parser_classes = (MultiPartParser, FormParser)  # Для обработки изображений
    permission_classes = (IsOwnerOnly,)
    
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
                    ReviewImageHotel.objects.create(review=review, image=image)

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
                    ReviewImageHotel.objects.create(review=review, image=image)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
