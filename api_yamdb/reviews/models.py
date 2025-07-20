from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .abstract_models import AbstractFeedback, DivisionAttributeModel

User = get_user_model()


def is_year_lte_now(year):
    """
    Метод валидации года выпуска произведения.
    Год не может быть больше текущего.
    """
    if year > timezone.now().year:
        raise ValidationError(
            f'{year} год больше {timezone.now().year}. ',
            'Нельзя добавить произведение с годом выпуска больше текущего!'
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
    К проиведению можно написать обзор (комментарий).
    """

    name = models.CharField(
        'Название',
        max_length=256,
        help_text='Введите название произведения (максимум 256 символов).'
    )
    year = models.IntegerField(
        'Год выпуска',
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

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if is_year_lte_now(year):
            return year


class Review(AbstractFeedback):
    """
    Модель обзора к произведению (Модели Title).
    Содержит автора, ссылку на произведение, текст, и дату создания.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Выберите автора обзора.'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Выберите произведение, к которому относится обзор.'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Укажите оценку произведения от 1 до 10.'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
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

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Выберите автора комментария.'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Выберите обзор, к которому относится комментарий.'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
