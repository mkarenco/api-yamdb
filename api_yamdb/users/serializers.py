from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import validate_reserved_username
from .models import ROLE_CHOICES

User = get_user_model()


class RegisterUserSerializer(serializers.Serializer):
    """
    Сериализатор для запроса кода подтверждения при регистрации.
    Принимает email и username.
    """

    email = serializers.EmailField(
        max_length=settings.EMAIL_LENGTH,
        required=True
    )
    username = serializers.CharField(
        max_length=settings.USERNAME_LENGTH,
        required=True
    )

    def validate_username(self, username):
        validate_reserved_username(username, raise_type='drf')
        return username


class UserSerializer(serializers.ModelSerializer):
    """
    выводит список пользователей, просмотр профиля и
    обновление данных пользователя.
    """

    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default='user',
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, username):
        validate_reserved_username(username, raise_type='drf')
        return username
