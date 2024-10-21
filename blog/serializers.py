from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Blog."""

    class Meta:
        model = Blog
        fields = "__all__"
