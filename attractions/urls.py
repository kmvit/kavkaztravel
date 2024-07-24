from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttractionViewSet

router = DefaultRouter()
router.register(r'attractions', AttractionViewSet)

app_name = 'attractions'

urlpatterns = [
    path('v1/', include(router.urls)),
]
