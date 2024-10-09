from rest_framework import serializers
from .models import DateTour, EstimationTour, GalleryTour, Guide, Order, Tag, Tour, TourOperator


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
        
class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели заказа тура.
    
    Этот класс отвечает за преобразование экземпляров модели Order
    в JSON и обратно, а также за валидацию входных данных.
    """
    
    class Meta:
        model = Order
        fields = ['id', 'tour', 'date', 'size', 'username', 'email', 'phone']
        
class OrderGetSerializer(OrderSerializer):
    """Сериализатор для модели заказа тура.
    
    Этот класс отвечает за преобразование экземпляров модели Order
    в JSON и обратно, а также за валидацию входных данных.
    """
    tour = TourGETSerializer()
    
class EstimationTourSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.
    
    Этот класс преобразует экземпляры модели EstimationTour
    в JSON и обратно, а также валидирует входные данные.
    """
  
    class Meta:
        model = EstimationTour
        fields = ['id', 'tour', 'estimation', 'feedback', 'image']
 
class EstimationTourGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели оценок и отзывов тура.
    
    Этот класс преобразует экземпляры модели EstimationTour
    в JSON и обратно, а также валидирует входные данные.
    """
    rating = serializers.SerializerMethodField()
    tour = TourGETSerializer()

    class Meta:
        model = EstimationTour
        fields = ['id', 'tour', 'estimation', 'feedback', 'image', 'date', "rating"]
    
    
    def get_rating(self, obj):
        estimations = EstimationTour.objects.filter(tour=obj.tour)
        total_estimation = len(estimations)
        sum_estimation = sum(est.estimation for est in estimations)
        if total_estimation>0:
            return round(sum_estimation / total_estimation, 2)
        return 10