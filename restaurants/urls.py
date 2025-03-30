from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantImageViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"meal", RestaurantViewSet)
router.register(r"restaurant-images", RestaurantImageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
