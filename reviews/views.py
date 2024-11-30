from rest_framework.decorators import action
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


from Kavkaztome.permissions import IsOwnerOnly
from .models import Review, ReviewPhoto
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = Review.objects.all()
    permission_classes = (IsOwnerOnly,)
    parser_classes = (MultiPartParser, FormParser)  # Для обработки изображений
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Фильтруем отзывы по объекту или пользователю, если переданы параметры.
        """
        queryset = Review.objects.all()
        content_type = self.request.query_params.get("content_type")
        object_id = self.request.query_params.get("object_id")
        if content_type and object_id:
            queryset = queryset.filter(
                content_type__model=content_type, object_id=object_id
            )
        return queryset

    def create(self, request, *args, **kwargs):
        # Создание отзыва
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем отзыв
            review = serializer.save(owner=self.request.user)

            # Если есть изображения, сохраняем их
            review_images = request.FILES.getlist("photos")
            if review_images:
                for image in review_images:
                    ReviewPhoto.objects.create(review=review, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Обновление существующего отзыва с новыми фотографиями.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            # Сначала обновляем отзыв
            instance = serializer.save()

            # Удаляем старые фотографии
            instance.photos.all().delete()

            # Сохраняем новые фотографии
            review_images = request.FILES.getlist("photos")
            if review_images:
                for image in review_images:
                    ReviewPhoto.objects.create(review=instance, image=image)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="all-ratings-for-object")
    def get_all_ratings_for_object(self, request, *args, **kwargs):
        """
        Получение всех рейтингов для конкретного объекта по его content_type и object_id.
        """
        content_type = request.query_params.get("content_type")
        object_id = request.query_params.get("object_id")
        # Проверка наличия обязательных параметров
        if not content_type or not object_id:
            return Response(
                {"detail": "content_type and object_id are required."}, status=400
            )

        try:
            # Получаем ContentType по названию модели
            content_type_instance = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            return Response({"detail": "Content type not found."}, status=400)
        except ValueError:
            return Response({"detail": "Invalid content_type value."}, status=400)

        # Фильтруем все отзывы по content_type и object_id
        reviews = Review.objects.filter(
            content_type=content_type_instance, object_id=object_id
        )

        if not reviews:
            return Response({"detail": "No reviews found for this object."}, status=404)

        # Сериализуем все отзывы
        serializer = ReviewSerializer(reviews, many=True)
        print(serializer.data)
        return Response(serializer.data)
