from rest_framework import viewsets
from django.shortcuts import get_object_or_404


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
