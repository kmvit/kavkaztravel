from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Entertainment
from .serializers import EntertainmentSerializer


class EntertainmentViewSet(viewsets.ModelViewSet):
    queryset = Entertainment.objects.all()
    serializer_class = EntertainmentSerializer
    permission_classes = (IsOwnerOnly,)
