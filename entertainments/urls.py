from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntertainmentViewSet

router = DefaultRouter()
router.register(r'entertainments', EntertainmentViewSet)

app_name = 'entertainments'

urlpatterns = [
    path('v1/', include(router.urls)),
]
