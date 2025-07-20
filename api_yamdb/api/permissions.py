from rest_framework import permissions


class IsAdminRoleOrRead(permissions.BasePermission):
    """
    Разрешает:
    - Читать всем.
    - Создавать/удалять объекты только пользователям-админам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminOrSeperUserRole(permissions.BasePermission):
    """Разрешает доступ, если пользователь аутентифицирован и он админ."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
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
            or request.user.is_moderator
            or request.user.is_admin
        )
