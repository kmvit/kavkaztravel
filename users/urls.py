from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, OwnerObjectsViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"owner_objects", OwnerObjectsViewSet, basename="owner_objects")
router.register(r"cabinet", OwnerObjectsViewSet, basename="cabinet")
urlpatterns = [
    path("v1/", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
