from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'rating', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
