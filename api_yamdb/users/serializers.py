from sqlite3 import IntegrityError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models
from .logic import _assign_confirmation_code, _send_confirmation_email


class UserSerializer(serializers.ModelSerializer):
    """
    выводит список пользователей, просмотр профиля и
    обновление данных пользователя
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=models.CustomUser.objects.all(),
                message='Пользователь с таким email уже существует'
            )
        ]
    )

    class Meta:
        model = models.CustomUser
        fields = '__all__'
        read_only_fields = ('role',)

    def update(self, instance, validated_data):
        if not (
            self.context['request'].user.is_staff
            and 'role' in validated_data
        ):
            raise serializers.ValidationError(
                'У вас недостаточно прав для изменения роли.'
            )
        return super().update(instance, validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запроса кода подтверждения при регистрации.
    Принимает email и username.
    """

    class Meta:
        model = models.CustomUser
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
            user, created = models.CustomUser.objects.get_or_create(
                username=validated_data['username'],
                defaults={'email': email, 'is_active': False}
            )
            if not created:
                if user.email != email:
                    raise serializers.ValidationError(
                        'Пользователь с таким username уже существует '
                        'и имеет другой email.'
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
