from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from hotels.models import Hotel
from hotels.serializers import HotelSerializer
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from tours.models import Guide, TourOperator
from tours.serializers import GuideSerializer, TourOperatorSerializer
from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import OwnerOrReadOnly


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class OwnerObjectsViewSet(viewsets.ViewSet):
    

    @action(detail=False, methods=['get', 'post', 'put', 'delete'])
    def hotels(self, request):
        if request.method == 'GET':
            hotels = Hotel.objects.filter(owner=request.user)
            serializer = HotelSerializer(hotels, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = HotelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == 'PUT':
            hotel = Hotel.objects.get(id=request.data['id'], owner=request.user)
            serializer = HotelSerializer(hotel, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            hotel = Hotel.objects.get(id=request.data['id'], owner=request.user)
            hotel.delete()
            return Response(status=204)

    @action(detail=False, methods=['get', 'post', 'put', 'delete'])
    def restaurants(self, request):
        if request.method == 'GET':
            restaurants = Restaurant.objects.filter(owner=request.user)
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == 'PUT':
            restaurant = Restaurant.objects.get(id=request.data['id'], owner=request.user)
            serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            restaurant = Restaurant.objects.get(id=request.data['id'], owner=request.user)
            restaurant.delete()
            return Response(status=204)

    @action(detail=False, methods=['get', 'post', 'put', 'delete'])
    def guides(self, request):
        if request.method == 'GET':
            guides = Guide.objects.filter(owner=request.user)
            print(guides, request.user.id)
            serializer = GuideSerializer(guides, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = GuideSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == 'PUT':
            guide = Guide.objects.get(id=request.data['id'], owner=request.user)
            serializer = GuideSerializer(guide, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            guide = Guide.objects.get(id=request.data['id'], owner=request.user)
            guide.delete()
            return Response(status=204)

    @action(detail=False, methods=['get', 'post', 'put', 'delete'])
    def touroperators(self, request):
        if request.method == 'GET':
            touroperators = TourOperator.objects.filter(owner=request.user)
            serializer = TourOperatorSerializer(touroperators, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = TourOperatorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        elif request.method == 'PUT':
            touroperator = TourOperator.objects.get(id=request.data['id'], owner=request.user)
            serializer = TourOperatorSerializer(touroperator, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            touroperator = TourOperator.objects.get(id=request.data['id'], owner=request.user)
            touroperator.delete()
            return Response(status=204)


class CabinetViewSet(viewsets.ViewSet):
    permission_classes = [OwnerOrReadOnly,]


    @action(detail=False, methods=['get', 'post', 'put', 'delete'])
    def guide(self, request):
        return OwnerObjectsViewSet.guides(self, request)
       