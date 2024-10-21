from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Attraction
from .serializers import AttractionSerializer


class AttractionViewSet(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    permission_classes = (IsOwnerOnly,)
