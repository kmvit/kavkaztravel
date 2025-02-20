from rest_framework import serializers
from .models import Booking, CustomUser, Notification, SMSVerification

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
        


from rest_framework import serializers
from .models import Booking
from django.contrib.contenttypes.models import ContentType

class BookingSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    user = serializers.StringRelatedField()  # You can also use PrimaryKeyRelatedField if needed.

    class Meta:
        model = Booking
        fields = '__all__'  # Include all fields of the Booking model

    def validate(self, data):
        """
        Add custom validation if needed (e.g., to ensure content model is valid)
        """
        content_model = data.get('content_type')
        if content_model and content_model.model not in Booking.VALID_CONTENT_MODELS:
            raise serializers.ValidationError(f"Тип объекта должен быть одним из: {', '.join(Booking.VALID_CONTENT_MODELS)}.")
        return data


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

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'message', 'is_read', 'created_at']
        

from rest_framework import serializers
from .models import UserNotificationChannel

class UserNotificationChannelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели UserNotificationChannel.
    """
    class Meta:
        model = UserNotificationChannel
        fields = ['id', 'user', 'channel_type']


