from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права доступа для администратора."""
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_staff)
        )


class IsAminOrReadOnly(permissions.BasePermission):
    """Права доступа для администратора или только для чтения."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_staff))
        )


class IsAuthorModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'moderator'
                         or request.user.is_admin
                         or request.user.is_staff
                         or obj.author == request.user))
        )
