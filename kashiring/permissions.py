from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает изменение и удаление только владельцу объекта.
    Остальные могут только просматривать (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS для всех (чтение)
        if request.method in SAFE_METHODS:
            return True

        # Разрешаем изменение и удаление только владельцу
        return obj.owner == request.user
