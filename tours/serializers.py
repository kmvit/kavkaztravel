from rest_framework import serializers


from rest_framework import serializers, viewsets
from .models import (
    TourOperator, Tour, GalleryTour,
    AvailableDateTour, Order, Tag
)
class TourOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperator
        fields = ['id', 'region', 'owner', 'license_number']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'tag_type']

class GalleryTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryTour
        fields = ['id', 'tour', 'image']

class AvailableDateTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDateTour
        fields = ['id', 'tour', 'start_date', 'end_date', 'is_active']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'tour', 'date', 'size', 'username', 'email', 'phone', 'owner']
class TourDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  
    gallery_tour = GalleryTourSerializer(many=True)  


    class Meta:
        model = Tour
        fields = ['id', 'guide', 'title', 'description', 'terms', 'region', 'tags', 'price', 'created_at', 'gallery_tour']

class TourCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    class Meta:
        model = Tour
        fields = ['id', 'guide', 'title', 'description', 'terms', 'region', 'tags', 'price']

    def validate_tags(self, value):
        # Проверяем, что все переданные теги существуют в базе данных
        if value:
            existing_tags = Tag.objects.filter(id__in=value)
            existing_tag_ids = existing_tags.values_list('id', flat=True)
            
            # Если переданные теги не совпадают с существующими тегами, выбрасываем ошибку
            missing_tags = set(value) - set(existing_tag_ids)
            if missing_tags:
                raise serializers.ValidationError(f"Некоторые теги не существуют: {', '.join(map(str, missing_tags))}!")
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        tour = Tour.objects.create(**validated_data)
        if tags_data:
            tour.tags.set(tags_data)  # Связываем теги с туром
        return tour

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags_data:
            instance.tags.set(tags_data)  # Связываем теги с туром
        instance.save()
        return instance
