from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Класс, который обеспечивает разрешения.

    При GET запросе - доступ разрешен всем.
    При PATCH, DELETE, POST - доступ разрешен только создателю объекта.
    """

    def has_permission(self, request, view):
        # Разрешаем доступ к всем для методов GET
        return (
            request.user.is_authenticated or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ к объекту только для его создателя
        if request.method in permissions.SAFE_METHODS:
            return True  # Доступ к объекту разрешен для GET-запросов
        return (
            obj.owner == request.user
        )  # Доступ к объекту разрешен только для создателя
