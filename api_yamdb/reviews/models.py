from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstract_models import AbstractFeedback, DivisionAttributeModel
# Для тесто нужно имя "validate_username"
from .validators import (
    is_year_lte_now, validate_reserved_username as validate_username
)


class MyUser(AbstractUser):
    """
    Расширенная модель пользователя.

    Добавлены поля:
    - username — псевдоним пользователя.
    - email — почта пользователя.
    - bio — информация о пользователе.
    - role — роль пользователя (пользователь, модератор, администратор).
    - confirmation_code — код подтверждения для регистрации/входа.
    """

    username = models.CharField(
        max_length=settings.USERNAME_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        help_text='Уникальный email пользователя.'
    )
    bio = models.TextField(
        'информация о пользователе',
        blank=True,
        null=True,
        help_text='Краткая информация о пользователе.'
    )
    role = models.CharField(
        'Роль',
        max_length=settings.ROLE_CHOICES_LENGTH,
        choices=settings.ROLE_CHOICES,
        default=settings.USER,
        help_text='Роль пользователя в системе.'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CODE_LENGTH,
        blank=True,
        null=True,
        help_text='Код подтверждения для регистрации или авторизации.'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:30]

    @property
    def is_admin(self):
        return (
            self.role == settings.ADMIN
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR


class Category(DivisionAttributeModel):
    """Модель объекта категории произведения."""

    class Meta(DivisionAttributeModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(DivisionAttributeModel):
    """Модель объекта жанра произведения."""

    class Meta(DivisionAttributeModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Модель объекта произведения (фильма, книги и т.п.).
    Объект модели может иметь несколько жанров и только одну категорию.
    Нельзя добавить произведение с годом выпуска в будущем.
    К произведению можно написать обзор (комментарий).
    """

    name = models.CharField(
        'Название',
        max_length=settings.NAME_LENGTH,
        help_text='Введите название произведения.'
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[is_year_lte_now],
        help_text='Укажите год выпуска произведения. Не может быть в будущем.'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
        help_text='Добавьте описание произведения.'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Выберите один или несколько жанров для произведения.'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        help_text='Выберите категорию произведения (опционально).'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:50]


class Review(AbstractFeedback):
    """
    Модель обзора к произведению (Модели Title).
    Содержит автора, ссылку на произведение, текст, и дату создания.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        help_text='Выберите произведение, к которому относится обзор.'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.MIN_SCORE),
            MaxValueValidator(settings.MAX_SCORE)
        ],
        help_text=(
            'Укажите оценку произведения '
            f'от {settings.MIN_SCORE} до {settings.MAX_SCORE}.'
        )
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review_author_title'
            )
        ]


class Comment(AbstractFeedback):
    """
    Модель комментария к обзору (Модели Review).
    Содержит автора, ссылку на обзор, текст, и дату создания.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        help_text='Выберите обзор, к которому относится комментарий.'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
