from rest_framework import permissions
from .models import CustomUser
class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user)
        owner = CustomUser.objects.get(username=request.user)
        return owner.user_type == 'guide'
        '''return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )'''

    def has_object_permission(self, request, view, obj):
        print(request.user)
        owner = CustomUser.objects.get(username=request.user)
        return owner.user_type == 'guide'