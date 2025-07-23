from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    decorators,
    filters,
    permissions,
    response,
    status,
    viewsets,
)
from rest_framework_simplejwt.tokens import AccessToken

from reviews import models
from . import serializers
from .filters import TitleFilter
from .logic import _confirmation_code, _send_confirmation_email
from .permissions import IsAdmin, IsAdminRoleOrRead, IsAuthorOrModeratorOrAdmin
from .viewsets import DivisionAttributeViewSet

User = get_user_model()


@decorators.api_view(('POST',))
def create_user_and_send_code(request):
    """Контроллер регистрации: всё взаимодействие с БД и отправка почты."""

    serializer = serializers.RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    confirmation_code = _confirmation_code()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    # Место для кэша
    # Узнай про нужно ли отправлять код зарегистрированному пользователю
    if not created: 
        user.confirmation_code = code
        user.save(update_fields=['confirmation_code'])

    user.confirmation_code = confirmation_code
    user.save(update_fields=['confirmation_code'])

    _send_confirmation_email(user.email, user.confirmation_code)

    return response.Response(
        {'username': user.username, 'email': user.email},
        status=status.HTTP_200_OK
    )


class UsersViewSet(viewsets.ModelViewSet):
    """
    API-эндпоинт для просмотра или редактирования профиля пользователя.
    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @decorators.action(
        detail=False,
        methods=('GET', 'PATCH'),
        url_path=settings.USER_SELF_PAGE,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def user_page(self, request):
        """
        Обрабатывает запросы к странице пользователя,
        позволяя просматривать и изменять его данные.
        """
        if request.method == 'GET':
            return response.Response(self.get_serializer(request.user).data)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return response.Response(serializer.data)


@decorators.api_view(('POST',))
def obtain_auth_token(request):
    """Функция для получения кода подтверждения."""

    serializer = serializers.TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    user = get_object_or_404(User.objects.get(username=username))

    return response.Response(
        {'token': str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK
    )


class TitleViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PATCH и DELETE):
    Обеспечивает фильтрацию произведений по имени, году выпуска,
    категории и жанрам (по слагу).
    Добавлять, редактировать и удалять произведения
    имеет право только пользователь-админитратор.
    """

    queryset = models.Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-rating')
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_class = TitleFilter
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'year', 'rating')
    ordering = ('-rating', 'name', 'year')
    permission_classes = (IsAdminRoleOrRead,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer


class CategoryViewSet(DivisionAttributeViewSet):
    """
    (GET, POST и DELETE):
    Создание и удаление категории, получение списка всех категорий.
    Добавлять, редактировать и удалять категории
    имеет право только пользователь-админитратор.
    """

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(DivisionAttributeViewSet):
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
    (GET, POST, PATCH и DELETE):
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
    permission_classes = (IsAuthorOrModeratorOrAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(models.Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    (GET, POST, PATCH и DELETE):
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
    permission_classes = (IsAuthorOrModeratorOrAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(models.Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
