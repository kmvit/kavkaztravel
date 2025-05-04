from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MessageViewSet,
    NotificationSettingsViewSet,
)

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'notification-settings', NotificationSettingsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]