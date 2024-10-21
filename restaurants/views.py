from rest_framework import viewsets

from Kavkaztome.permissions import IsOwnerOnly
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsOwnerOnly,)
