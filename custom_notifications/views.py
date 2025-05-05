from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message, NotificationSettings
from .serializers import NotificationSettingsSerializer
from .swagger_docs import NotificationSettingsSwagger


class NotificationSettingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления настройками уведомлений пользователя.
    """

    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAuthenticated]

    @NotificationSettingsSwagger.settings_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @NotificationSettingsSwagger.settings_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @NotificationSettingsSwagger.settings_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @NotificationSettingsSwagger.settings_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @NotificationSettingsSwagger.settings_partial_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @NotificationSettingsSwagger.settings_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
