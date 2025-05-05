from django.contrib import admin
from .models import Notification, Message, NotificationSettings


# Админка для модели Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("actor", "recipient", "timestamp", "unread")
    list_filter = ("unread", "timestamp")
    search_fields = ("actor__username", "recipient__username", "message")


# Админка для модели Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "created_at", "text")
    list_filter = ("created_at",)
    search_fields = ("sender__username", "receiver__username", "text")


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "email")
    list_filter = ("email",)
    search_fields = ("user__username",)
