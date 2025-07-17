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


class IsAdminRole(permissions.BasePermission):
    """Разрешает доступ если пользователь аутентифицирован и он админ."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешает:
    - Читать всем.
    - Создавать аутентифицированным пользователям.
    - Редактировать / удалять: автор, модератор или админ.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or getattr(request.user, 'is_moderator', False)
            or getattr(request.user, 'is_admin', False)
        )
