from rest_framework import viewsets

from Kavkaztome.permissions import IsOwnerOnly
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ресторанами.
    
    Обеспечивает стандартные операции CRUD 
    (создание, чтение, обновление, удаление)
    для модели Restaurant.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsOwnerOnly,)

