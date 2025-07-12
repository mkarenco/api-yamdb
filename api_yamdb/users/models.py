from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
]


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя.

    Добавлены поля:
    - bio — краткая биография
    - role — роль пользователя (пользователь, модератор, администратор)
    - confirmation_code — код подтверждения для регистрации/входа
    """
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
        help_text='Краткая информация о пользователе'
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        help_text='Роль пользователя в системе'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
        blank=True,
        null=True,
        help_text='Код подтверждения для регистрации или авторизации'
    )
    groups = models.ManyToManyField(
         Group,
         verbose_name='Группы',
         blank=True,
         related_name='custom_users',
         related_query_name='user',
         help_text='Группы к которым принадлежит пользователь'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Права пользователя',
        blank=True,
        related_name='custom_users',
        related_query_name='user',
        help_text='Специальные права для пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:30]
