from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantImageViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet)
router.register(r'restaurant-images', RestaurantImageViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
