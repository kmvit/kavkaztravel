from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Region
from .serializers import RegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления регионами.
    """

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsOwnerOnly,)