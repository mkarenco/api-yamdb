from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_reserved_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
]
ROLE_CHOICES_LENGTH = max(len(choice[0]) for choice in ROLE_CHOICES)


def validate_username(value):
    """
    Обёртка для validate_reserved_username в модели.
    Тесты ожидают найти функцию validate_username в users.models.
    """
    validate_reserved_username(value, raise_type='model')


class MyUser(AbstractUser):
    """
    Расширенная модель пользователя.

    Добавлены поля:
    - bio — краткая биография
    - role — роль пользователя (пользователь, модератор, администратор)
    - confirmation_code — код подтверждения для регистрации/входа
    """

    username = models.CharField(
        max_length=settings.USERNAME_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        help_text='Уникальный email пользователя'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='Краткая информация о пользователе'
    )
    role = models.CharField(
        'Роль',
        max_length=ROLE_CHOICES_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        help_text='Роль пользователя в системе'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CODE_LENGTH,
        blank=True,
        null=True,
        help_text='Код подтверждения для регистрации или авторизации'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:30]

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
