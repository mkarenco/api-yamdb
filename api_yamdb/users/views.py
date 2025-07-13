from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets, views, response

from .serializers import RegisterUserSerializer, UserSerializer

User = get_user_model()


class RegisterUserViewSet(views.APIView):
    """
    Вьюсет для регистрации нового пользователя.
    Принимает POST-запрос с данными:
    (email, username, password).
    """

    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            'Код подтверждения отправлен на вашу почту.',
            status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    """
    API-эндпоинт для просмотра или редактирования профиля пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'

    def get_object(self):
        """
        Возвращает аутентифицированного пользователя по эндпоинту me/
        В остальных случает обычный объект пользователя username
        """
        if self.kwargs.get(self.lookup_field) == 'me':
            return self.request.user
        return super().get_object()
