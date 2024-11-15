from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from Kavkaztome.permissions import IsOwnerOnly
from .models import Restaurant, ReviewRestaurant
from .serializers import (
    RestaurantSerializer,
    ReviewRestaurantGetSerializer,
    ReviewRestaurantSerializer,
)


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


class ReviewRestaurantViewSet(viewsets.ModelViewSet):
    """Класс для модели, который содержит оценки и отзывы."""

    queryset = ReviewRestaurant.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReviewRestaurantGetSerializer
        return ReviewRestaurantSerializer

    def perform_create(self, serializer):
        """Переопределяем метод perform_create для создания нового отзыва."""

        restaurant_id = self.request.data.get("restaurant")
        print(restaurant_id)
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        print(restaurant, 124)
        serializer.save(restaurant=restaurant, owner=self.request.user)

    def perform_update(self, serializer):
        """Переопределяем метод perform_update для обновления отзыва."""
        # Получаем ID тура из запроса или текущего объекта
        restaurant_id = self.request.data.get(
            "restaurant", self.get_object().restaurant.id
        )

        # Используем get_object_or_404 для получения тура
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # Сохраняем отзыв с обновленным туром
        serializer.save(restaurant=restaurant, owner=self.request.user)
