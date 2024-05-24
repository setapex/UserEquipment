from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method and permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdminReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id == view.kwargs.get('pk'):
            return True

        return bool(request.user.is_staff)