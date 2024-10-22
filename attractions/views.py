from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Attraction
from .serializers import AttractionSerializer


class AttractionViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра и редактирования экземпляров Attraction.

    Этот вьюсет предоставляет стандартные действия для управления 
    объектами аттрационов. Получение аттрационов может выполнять 
    любой пользователь, а создание, обновление и удаление доступны 
    только создателям объектов.
    """
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    permission_classes = (IsOwnerOnly,)
