from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

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
            {'message': 'Код подтверждения отправлен на вашу почту.'},
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
        """
        Возвращает аутентифицированного пользователя по эндпоинту me/
        В остальных случает обычный объект пользователя username
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        if lookup_value == 'me':
            return self.request.user
        return super().get_object()

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

