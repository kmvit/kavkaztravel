from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Blog.

    Этот сериализатор используется для преобразования данных блогов
    в формат JSON и обратно. Он позволяет сериализовать и десериализовать
    все поля модели Blog.
    """

    class Meta:
        model = Blog
        fields = "__all__"
