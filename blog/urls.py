from django.urls import path

from .views import BlogViewSet
from rest_framework.routers import DefaultRouter

# Create your views here.

router = DefaultRouter()
router.register(r"", BlogViewSet)


urlpatterns = [
    path(
        "/<slug:slug>/",
        BlogViewSet.as_view({"get": "retrieve"}),
        name="blog-detail",
    )
] + router.urls
