from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .abstract_models import AbstractFeedback, DivisionAttributeModel

User = get_user_model()

MIN_VALUE = 1
MAX_VALUE = 10


def is_year_lte_now(year):
    """
    Метод валидации года выпуска произведения.
    Год не может быть больше текущего.
    """
    if year > timezone.now().year:
        raise ValidationError(
            f'Год выпуска {year} не может быть больше текущего года ('
            f'{timezone.now().year}). '
            'Нельзя добавить произведение с годом выпуска в будущем.'
        )

    return True


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
        max_length=256,
        help_text='Введите название произведения (максимум 256 символов).'
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
        help_text='Добавьте описание произведения (опционально).'
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
        related_name='reviews',
        help_text='Выберите произведение, к которому относится обзор.'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ],
        help_text=f'Укажите оценку произведения от {MIN_VALUE} до {MAX_VALUE}.'
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
        related_name='comments',
        help_text='Выберите обзор, к которому относится комментарий.'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
