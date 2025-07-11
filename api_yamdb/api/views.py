from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from .viewsets import ListCreateDeleteViewSet
from reviews import models


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для запросов к модели Title."""

    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для запросов к модели Category."""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для запросов к модели Genre."""

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
