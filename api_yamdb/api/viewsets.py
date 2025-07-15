from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
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
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering_fields = ('name', 'slug')
    ordering = ('name', '-year')
    # Доработать права (Пользователь-админитратор)
    permission_classes = (IsAuthenticatedOrReadOnly,)
