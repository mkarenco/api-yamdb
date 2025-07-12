from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import UserSerializer, RegisterUserSerializer

User = get_user_model()

class RegisterUserViewSet(viewsets.GenericViewSet):
    """
    Вьюсет для запроса кода подтверждения при регистрации.
    Обрабатывает POST-запрос на 'auth/signup/'.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {"message": "Код подтверждения отправлен на вашу почту."},
            status=status.HTTP_200_OK
        )

class UsersViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт позволяющий пользователям просматривать или редактировать
    профиль пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        lookup_field = self.kwargs.get('lookup_field')
        if lookup_field == 'me':
            if self.request.user.is_authenticated:
                return self.request.user
            else:
                raise permissions.exceptions.NotAuthenticated(
                    'Аутентификация не предоставлена'
                )
        return super().get_object()

    def get_permissions(self):
        if (self.action in ['retrieve', 'update', 'partial_update'] and
                self.kwargs.get(self.lookup_field) == 'me'):
            return [permissions.IsAuthenticated()]

        if self.action == 'list':
            return [permissions.IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]

        return [permissions.IsAuthenticated()]

