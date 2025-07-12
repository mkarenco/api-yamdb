import secrets
from sqlite3 import IntegrityError

from django.core.mail import send_mail
from rest_framework import serializers

from api_yamdb import settings
from . import models
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    Используется для вывода списка пользователей
    и детальной информации о пользователе.
    """

    class Meta:
        model = models.CustomUser
        fields = '__all__'
        read_only_fields = ('role',)

    def update(self, instance, validated_data):
        if not self.context['request'].user.is_staff and 'role' in validated_data:
            raise serializers.ValidationError({
                'role': 'У вас недостаточно прав для изменения роли.'
            })
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

    def validate_email(self, value):
        """
        Проверка email на наличие в базе
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return value

    def create(self, validated_data):
        """

        """
        username = validated_data['username']
        email = validated_data['email']

        try:
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={'email': email, 'is_active': False}
            )
            if not created:
                if user.email != email:
                    raise serializers.ValidationError(
                        'Пользователь с таким username уже существует'
                        ' и имеет другой email'
                    )
                if user.is_active:
                    raise serializers.ValidationError(
                        "Пользователь уже активен."
                    )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с таким username или email уже существует.'
            )
        confirmation_code = ''.join(secrets.choice('0123456789ABCDEFG')
                                    for _ in range(6))
        user.confirmation_code = confirmation_code

        try:
            send_mail(
                'Код подтверждения для регистрации',
                f'Ваш код подтверждения: {confirmation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            raise serializers.ValidationError(f"Ошибка отправки письма: {e}")

        return user