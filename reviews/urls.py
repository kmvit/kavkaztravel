from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarReviewViewSet, CarReviewImageViewSet


router = DefaultRouter()
router.register(r"car", CarReviewViewSet, basename="car")
router.register(r"car-images", CarReviewImageViewSet, basename="car-image")

urlpatterns = [
    path("", include(router.urls)),
]
