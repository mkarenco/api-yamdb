from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование и удаление только автору объекта.
    Остальные пользователи могут только читать.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """Права доступа для администратора."""
    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_authenticated and request.user.is_admin
        )


class IsModerator(permissions.BasePermission):
    """
    Если пользователь аутентифицирован, он модератор, он может
    изменять, удалять комментарии/обзоры.
    """
    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_authenticated
                and request.user.role == 'moderator'
                and request.method in ('PUT', 'PATCH', 'DELETE')
        )


