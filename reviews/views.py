from rest_framework import viewsets, permissions

from Kavkaztome.permissions import IsOwnerOnly
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOnly,)

    def perform_create(self, serializer):
        """
        Переопределяем метод perform_create.
        """
        serializer.save(owner=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Переопределяем метод perform_update.
        """
        serializer.save(owner=self.request.user)
        return Response(status=status.HTTP_200_OK)
