from sqlite3 import IntegrityError

from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from django.core.validators import RegexValidator

from .logic import _assign_confirmation_code, _send_confirmation_email
from .models import ROLE_CHOICES

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запроса кода подтверждения при регистрации.
    Принимает email и username.
    """

    email = serializers.EmailField(
        max_length=254,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже существует'
            )
        ]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Имя пользователя содержит недопустимые символы'
            ),
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким username уже существует'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email',)
        read_only_fields = ('role',)

    def validate_username(self, value):
        """
        Проверка имени пользователя на запрещенный username: me
        """
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username нельзя'
            )
        return value

    def create(self, validated_data):
        """
        Создание пользователя с неактивным состоянием по умолчанию.
        """
        email = validated_data['email']
        try:
            user, created = User.objects.get_or_create(
                username=validated_data['username'],
                defaults={'email': email, 'is_active': False}
            )
            if not created:
                if user.email != email:
                    raise serializers.ValidationError(
                        'Пользователь с таким email уже существует'
                    )
                if user.is_active:
                    raise serializers.ValidationError(
                        'Пользователь уже активен.'
                    )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с таким username или email уже существует.'
            )
        confirmation_code = _assign_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
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

    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Имя пользователя содержит недопустимые символы'
            )
        ]
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
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

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request.user.is_admin and 'role' in validated_data:
            raise serializers.ValidationError(
                'У вас недостаточно прав для изменения роли.'
            )
        return super().update(instance, validated_data)
