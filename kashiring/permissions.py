from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает изменение и удаление только владельцу объекта.
    Остальные могут только просматривать.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if request.method in ["PATCH", "PUT", "DELETE"]:
            return obj.owner == request.user
