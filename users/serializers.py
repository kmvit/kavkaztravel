from rest_framework import serializers
from .models import CustomUser, SMSVerification


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "bio"]


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = CustomUser
        fields = ["user", "bio", "avatar", "phone_number"]


class SMSVerificationSerializer(serializers.ModelSerializer):
    """

    Этот сериализатор используется для представления и обработки данных, связанных с процессом
    верификации номера телефона через SMS. Модель SMSVerification хранит информацию о статусе
    отправленных кодов подтверждения и сроках их действия.
    """

    class Meta:
        model = SMSVerification
        fields = [
            "id",
            "phone_number",
            "verification_code",
            "message_id",
            "status",
            "created_at",
            "expires_at",
        ]
