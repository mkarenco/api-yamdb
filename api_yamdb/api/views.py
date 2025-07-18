from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from reviews import models
from . import serializers
from .custom_permissions import IsAdminRole, IsAuthorModeratorOrAdmin
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
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'year', 'rating')
    ordering = ('-rating', 'name', 'year')

    def get_permissions(self):
        if self.action in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (IsAdminRole(),)


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    (GET, POST и DELETE):
    Создание и удаление категории, получение списка всех категорий.
    Добавлять, редактировать и удалять категории
    имеет право только пользователь-админитратор.
    """

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """
    (GET, POST и DELETE):
    Создание и удаление жанра, получение списка всех жанров.
    Добавлять, редактировать и удалять жанры
    имеет право только пользователь-админитратор.
    """

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PUT, PATCH и DELETE):
    получаем, отправляем, редактируем или удаляем проиведения.
    """

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('author__username', 'title__name')
    search_fields = ('text', 'author__username', 'title__name')
    ordering_fields = ('score', 'pub_date')
    ordering = ('-pub_date',)
    permission_classes = (IsAuthorModeratorOrAdmin,)

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


class CommentViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PUT, PATCH и DELETE):
    получаем, отправляем, редактируем или удаляем комментарии к обзорам.
    """

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('author__username',)
    search_fields = ('text', 'author__username', 'title__name')
    ordering_fields = ('pub_date',)
    ordering = ('-pub_date',)
    permission_classes = (IsAuthorModeratorOrAdmin,)

    def get_review(self):
        return get_object_or_404(models.Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
