from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import (
    permissions,
    status,
    viewsets,
    filters,
    response,
    decorators,
    exceptions
)


from .logic import _assign_confirmation_code, _send_confirmation_email
from api.permissions import IsAdmin
from . import serializers

User = get_user_model()


@decorators.api_view(('POST',))
def register_user(request):
    """
    Контроллер регистрации: всё взаимодействие с БД и отправка почты.
    """

    serializer = serializers.RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    if User.objects.filter(email=email).exclude(username=username).exists():
        raise exceptions.ValidationError(
            {'email': 'Пользователь с таким email уже существует.'}
        )

    confirmation_code = _assign_confirmation_code()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_active': False,
            'confirmation_code': confirmation_code,
        }
    )

    if not created:
        if user.email != email:
            raise exceptions.ValidationError(
                {'email': 'Неверный email для этого username.'}
            )
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
        data = request.data.copy()
        data.pop('role', None)
        serializer = self.get_serializer(
            request.user,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


@decorators.api_view(('POST',))
def obtain_auth_token(request):
    """
    Функция для получения кода подтверждения.
    """
    username = request.data.get('username')
    code = request.data.get('confirmation_code')

    if not username or not code:
        raise exceptions.ValidationError(
            {'detail': 'username и confirmation_code обязательны'}
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise exceptions.NotFound(
            {'username': 'Пользователь не найден'}
        )

    if user.confirmation_code != code:
        raise exceptions.ValidationError(
            {'confirmation_code': 'Неверный код подтверждения!'}
        )

    # КОД ПОДТВЕРЖДЕНИЯ ПРОВЕРЕН — удаляем его, чтобы был одноразовым
    user.confirmation_code = ''
    return response.Response(
        {'token': str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK
    )
