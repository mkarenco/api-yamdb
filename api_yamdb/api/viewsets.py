from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from .custom_permissions import IsAdminRoleOrRead


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Базовый абстрактный ViewSet для операций:
    - получения списка объектов (list),
    - создания нового объекта (create),
    - удаления объекта (destroy).

    Дополнительно использует:
    - поиск по полям,
    - фильтрацию,
    - сортировку,
    -  поиск объекту по слаг.
    """

    lookup_field = 'slug'
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering_fields = ('name', 'slug')
    ordering = ('name',)
    permission_classes = (IsAdminRoleOrRead,)
