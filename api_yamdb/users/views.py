from django.contrib.auth import get_user_model
from rest_framework import permissions, response, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.throttling import ScopedRateThrottle

from .serializers import RegisterUserSerializer, UserSerializer
from api.custom_permissions import IsAdmin

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
    lookup_field = 'username'
    # доделать логику по доступу аутентифированному пользователю
    def get_object(self):
        """
        Возвращает аутентифицированного пользователя по эндпоинту me/
        В остальных случает обычный объект пользователя username
        """
        if self.kwargs.get(self.lookup_field) == 'me':
            return self.request.user
        return super().get_object()


class UserObtainAuthToken(views.APIView):
    """
    View для получения кода подтверждения.
    Проверяется наличие пользователя по username
    Проводится проверка отправленного пользователем кода подтверждения.
    """

    permission_classes = (permissions.AllowAny,)
    # Ограничение ввода кода подтверждения, чтобы избежать перебора
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'message_send_limit'

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response(
                {'error': 'username и confirmation_code обязательны.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
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
