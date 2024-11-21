
from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Entertainment, ReviewEntertainment, ReviewImageEntertainment
from .serializers import (
    EntertainmentSerializer,
    ReviewEntertainmentSerializer,
)


class EntertainmentViewSet(viewsets.ModelViewSet):
    queryset = Entertainment.objects.all()
    serializer_class = EntertainmentSerializer
    permission_classes = (IsOwnerOnly,)

from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
class ReviewEntertainmentViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = ReviewEntertainment.objects.all()
    serializer_class = ReviewEntertainmentSerializer
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
                    ReviewImageEntertainment.objects.create(review=review, image=image)

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
                    ReviewImageEntertainment.objects.create(review=review, image=image)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
