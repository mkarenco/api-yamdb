from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model
    """
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
        help_text="Краткая информация о пользователе"
    ),

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES_CHOISES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES_CHOISES,
        default=USER,
        help_text='Роль пользователя в системе'
    )
    confirmation_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        'auth.Group',
         verbose_name='группы',
         blank=True,
         related_name='customuser_set',
         related_query_name='user',
         help_text='группы к которым принадлежит пользователь'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='права пользователя',
        blank=True,
        related_name='customuser_set',
        related_query_name='user',
        help_text='специальные права для пользователя'
    )


    class Meta():
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.username
