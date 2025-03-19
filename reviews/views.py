from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CarReview, CarReviewImage
from .serializers import (
    CarReviewDetailSerializer,
    CarReviewCreateUpdateSerializer,
    CarReviewImageSerializer,
)
from .pagination import ReviewPagination
from .permissions import IsOwnerOrReadOnly
from .swagger_schemas import (
    car_review_create,
    car_review_list,
    car_review_detail,
    car_review_update,
    car_review_replace,
    car_review_delete,
    car_review_image_upload,
    car_review_image_list,
    car_review_image_detail,
    car_review_image_update,
    car_review_image_delete,
)

class CarReviewViewSet(viewsets.ModelViewSet):
    """CRUD для отзывов (GET – с фото и оценками, POST/PUT – без фото) автомобиля."""

    queryset = CarReview.objects.select_related("user", "car").prefetch_related(
        "ratings", "car_images"
    )
    pagination_class = ReviewPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Фильтрация: админ видит всё, пользователи – только одобренные отзывы автомобиля."""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(is_approved=True)

    def get_serializer_class(self):
        """Используем разные сериализаторы для GET и POST/PUT автомобиля."""
        if self.action in ["list", "retrieve"]:
            return CarReviewDetailSerializer  # GET-запрос → полный обзор
        return CarReviewCreateUpdateSerializer  # POST/PUT → только текст + оценки

    @car_review_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @car_review_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @car_review_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @car_review_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @car_review_replace
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @car_review_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CarReviewImageViewSet(viewsets.ModelViewSet):
    """CRUD для загрузки изображений к отзывам автомобиля."""

    queryset = CarReviewImage.objects.all()
    serializer_class = CarReviewImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    @car_review_image_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @car_review_image_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @car_review_image_upload
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @car_review_image_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @car_review_image_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
