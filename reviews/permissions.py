from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - Только аутентифицированные пользователи могут создавать отзывы.
    - Анонимные пользователи могут только читать (GET).
    - Только владелец может редактировать и удалять отзыв.
    """

    def has_permission(self, request, view):
        """Глобальное разрешение: чтение - всем, создание - только авторизованным"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Операции с объектом: только владелец может редактировать/удалять"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
