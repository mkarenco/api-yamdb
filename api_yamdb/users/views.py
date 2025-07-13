from django.contrib.auth import get_user_model
from rest_framework import permissions, response, status, views, viewsets
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser
from .serializers import UserSerializer, RegisterUserSerializer

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

    def get_permissions(self):
        return (permissions.IsAuthenticated(),)


class UserObtainAuthToken(views.APIView):
    """
    API эндпоинт для получения кода подтверждения.
    Проверяется наличие пользователя по username в случае отсутвия
    пользователя возвращается ответ 404 NOT FOUND
    Проводится проверка отправленного пользователем кода подтверждения
    если не совпадает отправленный и введеный код возвращается
    ответ 400 BAD REQUEST
    В остальных случаях возвращается 200 OK
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(
                'Пользователь не найден.',
                status=status.HTTP_404_NOT_FOUND
            )

        if user.confirmation_code != confirmation_code:
            return Response(
                'Неправильный код подтверждения!',
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.save()
        token = str(AccessToken.for_user(user))
        return Response({
            'token': token
        },
            status=status.HTTP_200_OK
        )
