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


class IsAdminRoleUser(permissions.BasePermission):
    """
    Разрешает добавление и удаление объектов только
    пользователям c ролью (role) 'admin'.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role() == 'admin'
        )
