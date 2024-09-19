from rest_framework import permissions
from .models import CustomUser
from django.shortcuts import get_object_or_404

class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        owner = get_object_or_404(CustomUser, username=request.user)
        return owner.user_type == 'guide'
       

    def has_object_permission(self, request, view, obj):
        owner = get_object_or_404(CustomUser, username=request.user)
        return owner.user_type == 'guide'