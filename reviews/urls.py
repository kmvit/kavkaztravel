from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarReviewViewSet, CarReviewImageViewSet

# Создаём роутер для автоматической генерации маршрутов
router = DefaultRouter()
router.register(r"car", CarReviewViewSet, basename="car")  # Отзывы
router.register(r"car-images", CarReviewImageViewSet, basename="car-image")  # Изображенияc

urlpatterns = [
    path("", include(router.urls)),  # Подключаем все маршруты из роутера
]
