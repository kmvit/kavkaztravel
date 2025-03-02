from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Review, ReviewImage, Rating
from .serializers import ReviewDetailSerializer, ReviewCreateUpdateSerializer, ReviewImageSerializer, RatingSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD для отзывов (GET – с фото и оценками, POST/PUT – без фото)"""
    queryset = Review.objects.select_related('user', 'car').prefetch_related('ratings', 'images')

    def get_queryset(self):
        """Фильтрация: админ видит всё, пользователи – только одобренные отзывы"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(is_approved=True)

    def get_serializer_class(self):
        """Используем разные сериализаторы для GET и POST/PUT"""
        if self.action in ['list', 'retrieve']:
            return ReviewDetailSerializer  # GET-запрос → полный обзор
        return ReviewCreateUpdateSerializer  # POST/PUT → только текст + оценки

class ReviewImageViewSet(viewsets.ModelViewSet):
    """CRUD для загрузки изображений"""
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer
    parser_classes = (MultiPartParser, FormParser)  # Позволяет загружать фото через multipart/form-data

class RatingViewSet(viewsets.ModelViewSet):
    """CRUD для оценок"""
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
