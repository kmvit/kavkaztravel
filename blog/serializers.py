from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Blog
        fields = fields = (
            "id",
            "title",
            "slug",
            "photo",
            "content",
            "created_at",
            "updated_at",
            "published",
        )
 