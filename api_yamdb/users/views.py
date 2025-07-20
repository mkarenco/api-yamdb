from django.contrib.auth import get_user_model
from rest_framework import (
    permissions,
    status,
    views,
    viewsets,
    filters,
    response,
    decorators
)

from api.permissions import IsAdminOrSeperUserRole
from . import serializers


User = get_user_model()


class RegisterUserViewSet(views.APIView):
    """
    Вьюсет для регистрации нового пользователя.
    Принимает POST-запрос с данными:
    (email, username, password).
    """

    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterUserSerializer(data=request.data)
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
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOrSeperUserRole,)
    http_method_names = ('get', 'post', 'patch', 'delete')

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
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.save()
        return response.Response(token_data, status=status.HTTP_200_OK)
