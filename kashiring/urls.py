from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CarImageViewSet, RentalConditionViewSet

app_name = "kashiring"

# Создаем роутер и регистрируем в нем наши viewsets
router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'car-images', CarImageViewSet, basename='car-image')
router.register(r'rental-conditions', RentalConditionViewSet, basename='rental-condition')

urlpatterns = [
    path('', include(router.urls)),
]