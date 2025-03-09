from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarViewSet,
    CarImageViewSet,
    RentalConditionViewSet,
    RentalCreateView,
    RentalDiscountViewSet,
    CarOptionViewSet,
    CarEquipmentViewSet,
)

app_name = "kashiring"

# Создаем роутер и регистрируем в нем наши viewsets
router = DefaultRouter()
router.register(r"cars", CarViewSet, basename="car")
router.register(r"car-images", CarImageViewSet, basename="car-image")
router.register(
    r"rental-conditions", RentalConditionViewSet, basename="rental-condition"
)
router.register(r"discounts", RentalDiscountViewSet, basename="rentaldiscount")
router.register(r"car-options", CarOptionViewSet, basename="car-option")
router.register(r"car-equipment", CarEquipmentViewSet, basename="car-equipment")  

urlpatterns = [
    path("", include(router.urls)),
    path("rental/create/", RentalCreateView.as_view(), name="rental-create"),
]
