from rest_framework import serializers
from .models import NotificationSettings


class NotificationSettingsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = NotificationSettings
        fields = ["id", "user", "email"]
        extra_kwargs = {
            "user": {"write_only": True},
            "email": {"help_text": "Получать уведомления по электронной почте"},
        }

    def validate(self, data):

        if self.instance is None:  # Только при создании (POST)
            if NotificationSettings.objects.filter(user=data["user"]).exists():
                raise serializers.ValidationError(
                    "Настройки уже существуют для этого пользователя."
                )
        return data

    def update(self, instance, validated_data):
        validated_data.pop("user", None)
        return super().update(instance, validated_data)
