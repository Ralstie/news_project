from rest_framework.permissions import BasePermission

from .models import User


class IsJournalistOrReadOnly(BasePermission):    

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == User.Role.JOURNALIST
        )


class IsEditorOrReadOnly(BasePermission):   

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == User.Role.EDITOR
        )