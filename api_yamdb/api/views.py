from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from reviews import models


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для запросов к модели Title.
    Обеспечивает фильтрацию произведений по имени, году выпуска,
    категории и жанрам (по слагу).
    Добавлять, редактировать и удалять произведения
    имеет право только пользователь-админитратор.
    """

    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для запросов к модели Category.
    Поддерживает методы GET, POST и DELETE.
    Создание и удаление категории, получение списка всех категорий.
    Добавлять, редактировать и удалять категории
    имеет право только пользователь-админитратор.
    """

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для запросов к модели Genre.
    Поддерживает методы GET, POST и DELETE.
    Создание и удаление жанра, получение списка всех жанров.
    Добавлять, редактировать и удалять жанры
    имеет право только пользователь-админитратор.
    """

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RegisterUserViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для регистрации и аутентификации пользователей
    """
    pass


class UsersViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт позволяющий пользователям просматривать или редактировать
    """
    pass

# Все что выше перенести в приложение users


from rest_framework import permissions, pagination, viewsets
from django.shortcuts import get_object_or_404

from . import serializers
from .permissions import IsAuthorOrReadOnly
from reviews.models import Reviews, Title


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PUT, PATCH, DELETE):
    получаем, отправляем, редактируем или удаляем проиведения.
    """
    queryset = Reviews.objects.all()
    serializer_class = serializers.ReviewsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )
    pagination_class = pagination.PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
