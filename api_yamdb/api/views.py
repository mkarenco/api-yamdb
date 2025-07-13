from django.shortcuts import get_object_or_404
from rest_framework import filters, pagination, permissions, viewsets

from reviews import models
from . import custom_permissions, serializers
from .utils import update_rating
from .viewsets import ListCreateDeleteViewSet


class TitleViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PUT, PATCH и DELETE):
    Обеспечивает фильтрацию произведений по имени, году выпуска,
    категории и жанрам (по слагу).
    Добавлять, редактировать и удалять произведения
    имеет право только пользователь-админитратор.
    """

    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    # Доработать права (Пользователь-админитратор)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    (GET, POST и DELETE):
    Создание и удаление категории, получение списка всех категорий.
    Добавлять, редактировать и удалять категории
    имеет право только пользователь-админитратор.
    """

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    # Доработать права (Пользователь-админитратор)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GenreViewSet(ListCreateDeleteViewSet):
    """
    (GET, POST и DELETE):
    Создание и удаление жанра, получение списка всех жанров.
    Добавлять, редактировать и удалять жанры
    имеет право только пользователь-админитратор.
    """

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    # Доработать права (Пользователь-админитратор)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PUT, PATCH, DELETE):
    получаем, отправляем, редактируем или удаляем проиведения.
    """

    queryset = models.Reviews.objects.all()
    serializer_class = serializers.ReviewsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsAuthorOrReadOnly
    )
    pagination_class = pagination.PageNumberPagination

    def get_title(self):
        return get_object_or_404(models.Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
        update_rating(self.get_title())

    def perform_update(self, serializer):
        serializer.save()
        update_rating(self.get_title())

    def perform_destroy(self, instance):
        instance.delete()
        update_rating(self.get_title())
