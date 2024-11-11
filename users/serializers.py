from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "bio"]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = CustomUser
        fields = ["user", "bio", "avatar", "phone_number"]

# sms/serializers.py

from rest_framework import serializers
from .models import SMSVerification

class SMSVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSVerification
        fields = ['id', 'phone_number', 'verification_code', 'message_id', 'status', 'created_at', 'expires_at']
