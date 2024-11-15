from django.shortcuts import get_object_or_404
from Kavkaztome.permissions import IsOwnerOnly
from rest_framework import viewsets
from .models import Entertainment, ReviewEntertainment
from .serializers import (
    EntertainmentSerializer,
    ReviewEntertainmentGetSerializer,
    ReviewEntertainmentSerializer,
)


class EntertainmentViewSet(viewsets.ModelViewSet):
    queryset = Entertainment.objects.all()
    serializer_class = EntertainmentSerializer
    permission_classes = (IsOwnerOnly,)


class ReviewEntertainmentViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = ReviewEntertainment.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewEntertainmentGetSerializer
        return ReviewEntertainmentSerializer

    def perform_create(self, serializer):
        """Переопределяем метод perform_create для создания нового отзыва."""

        entertainment_id = self.request.data.get("entertainment")
        entertainment = get_object_or_404(Entertainment, id=entertainment_id)
        serializer.save(entertainment=entertainment, owner=self.request.user)

    def perform_update(self, serializer):
        """Переопределяем метод perform_update для обновления отзыва."""
        # Получаем ID тура из запроса или текущего объекта
        entertainment_id = self.request.data.get(
            "entertainment", self.get_object().entertainment.id
        )

        # Используем get_object_or_404 для получения тура
        entertainment = get_object_or_404(Entertainment, id=entertainment_id)

        # Сохраняем отзыв с обновленным туром
        serializer.save(entertainment=entertainment, owner=self.request.user)
