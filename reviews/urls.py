from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewImageViewSet

# Создаём роутер для автоматической генерации маршрутов
router = DefaultRouter()
router.register(r"car", ReviewViewSet, basename="car")  # Отзывы
router.register(r"car-images", ReviewImageViewSet, basename="car-image")  # Изображенияc

urlpatterns = [
    path("", include(router.urls)),  # Подключаем все маршруты из роутера
]
