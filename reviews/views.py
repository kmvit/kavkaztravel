from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Review, ReviewImage
from .serializers import (
    ReviewDetailSerializer,
    ReviewCreateUpdateSerializer,
    ReviewImageSerializer,
)
from .pagination import ReviewPagination
from .permissions import IsOwnerOrReadOnly
from .swagger_schemas import (
    review_create,
    review_list,
    review_detail,
    review_update,
    review_replace,
    review_delete,
    review_image_upload,
    review_image_list,
    review_image_detail,
    review_image_update,
    review_image_delete,
)


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD для отзывов (GET – с фото и оценками, POST/PUT – без фото)"""

    queryset = Review.objects.select_related("user", "car").prefetch_related(
        "ratings", "images"
    )
    pagination_class = ReviewPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Фильтрация: админ видит всё, пользователи – только одобренные отзывы"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(is_approved=True)

    def get_serializer_class(self):
        """Используем разные сериализаторы для GET и POST/PUT"""
        if self.action in ["list", "retrieve"]:
            return ReviewDetailSerializer  # GET-запрос → полный обзор
        return ReviewCreateUpdateSerializer  # POST/PUT → только текст + оценки

    @review_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @review_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @review_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @review_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @review_replace
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @review_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ReviewImageViewSet(viewsets.ModelViewSet):
    """CRUD для загрузки изображений к отзывам"""

    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    @review_image_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @review_image_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @review_image_upload
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @review_image_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @review_image_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
