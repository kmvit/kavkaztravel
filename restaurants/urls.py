from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
