from rest_framework import serializers
from .models import DateTour, GalleryTour, Guide, Tag, Tour, TourOperator


class GuideSerializer(serializers.ModelSerializer):
    owner =serializers.StringRelatedField(read_only=True)# serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Guide
        fields = '__all__'


class TourOperatorSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)#serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TourOperator
        fields = '__all__'
        
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        
        
class TourGETSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    tour_operator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tour
        fields = ('id', 'name', "description",  "seo_title", "seo_description", "tag", 'tour_operator')
   

class TourSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tour
        fields = ('id', 'name', "description",  "seo_title", "seo_description", "tag", 'tour_operator')
   


class GalleryTourSerializer(serializers.ModelSerializer):
    tour = TourGETSerializer()
    class Meta:
        model = GalleryTour
        fields = ('id', 'tour', 'image')
        
      
class DateTourrSerializer(serializers.ModelSerializer):
    tour = TourGETSerializer()

    class Meta:
        model = DateTour
        fields = ('id', 'tour', 'begin_date', 'end_date', 'is_free')
        