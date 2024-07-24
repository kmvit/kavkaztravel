from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet

app_name = 'regions'

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='regions')

urlpatterns = [
    path('v1/', include(router.urls)),
]
