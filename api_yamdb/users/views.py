from django.contrib.auth import get_user_model
from rest_framework import (
    decorators,
    permissions,
    response,
    status,
    views,
    filters,
    viewsets,
)
from rest_framework_simplejwt.tokens import AccessToken

from api.custom_permissions import IsAdminOrSeperUserRole
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
        user = serializer.save()
        return response.Response({
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """
    API-эндпоинт для просмотра или редактирования профиля пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOrSeperUserRole,)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return response.Response(
                {'detail': 'Метод PUT запрещён.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)

    @decorators.action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """
        Обрабатывает запросы к 'me/' — возвращает профиль пользователя,
        позволяя просматривать и изменять его данные.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return response.Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)


class UserObtainAuthToken(views.APIView):
    """
    View для получения кода подтверждения.
    Проверяется наличие пользователя по username
    Проводится проверка отправленного пользователем кода подтверждения.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return response.Response(
                {'error': 'username и confirmation_code обязательны.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return response.Response(
                {'error': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.confirmation_code != confirmation_code:
            return response.Response(
                {'error': 'Неправильный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = True
        user.save()
        token = str(AccessToken.for_user(user))
        return response.Response({
            'token': token
        },
            status=status.HTTP_200_OK
        )
