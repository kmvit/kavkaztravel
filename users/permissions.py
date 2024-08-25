from rest_framework import permissions
from .models import CustomUser
class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        owner = CustomUser.objects.get(username=request.user)
        return owner.user_type == 'guide'
       

    def has_object_permission(self, request, view, obj):
        owner = CustomUser.objects.get(username=request.user)
        return owner.user_type == 'guide'