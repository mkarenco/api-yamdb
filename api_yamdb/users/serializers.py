import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import AccessToken

from .logic import _assign_confirmation_code, _send_confirmation_email
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
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Имя пользователя содержит недопустимые символы'
            )
        ]
    )

    def validate_username(self, username):
        """
        Проверка имени пользователя на запрещенный username: me
        """
        if username == settings.USER_SELF_PAGE:
            raise serializers.ValidationError(
                f'Использовать имя {settings.USER_SELF_PAGE} нельзя'
            )
        return username

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']

        email_owner = User.objects.filter(email=email).first()
        if email_owner and email_owner.username != username:
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким email уже существует.'}
            )
        try:
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError(
                    {'email': 'Неверный email для этого username.'}
                )
            confirmation_code = _assign_confirmation_code()
            user.confirmation_code = confirmation_code
            user.save()
        except User.DoesNotExist:
            user = User.objects.create(
                username=username,
                email=email,
                is_active=False,
                confirmation_code=_assign_confirmation_code()
            )
        try:
            _send_confirmation_email(user.email, user.confirmation_code)
        except Exception as e:
            raise serializers.ValidationError(
                f'Ошибка отправки письма: {e}'
            )
        return user


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
        if not re.fullmatch(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                'Имя пользователя содержит недопустимые символы'
            )
        return username


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs.get('username'))
        except User.DoesNotExist:
            raise exceptions.NotFound(
                {'username': 'Пользователь не найден.'}
            )

        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'}
            )
        return attrs['user']

    def create(self, validated_data):
        user = validated_data['user']
        if not user.is_active:
            user.is_active = True
            user.save()
        token = str(AccessToken.for_user(user))
        return {'token': token}
