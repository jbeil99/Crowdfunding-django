from rest_framework.permissions import BasePermission
from .models import Project


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.user == request.user or request.user.is_staff
        return False
