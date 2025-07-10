from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def check_length(string, max_length=30):
    """
    Метод проверки длины строки.
    Если строка длиннее допустимого, возвращает фрагмент строки + '...'.
    """
    return string[:max_length] + '...' if len(string) > max_length else string


class AttributeModel(models.Model):
    """Абстрактная модель свойства объекта."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return check_length(self.name)


class Category(AttributeModel):
    """Модель объекта категории произведения."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AttributeModel):
    """Модель объекта категории произведения."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Модель объекта произведения (фильма, книги и т.п.).
    Объект модели может иметь несколько жанров и только одну категорию.
    Нельзя добавить произведение с годом выпуска в будущем.
    """

    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return check_length(self.name)

    def clean(self):
        if self.year > timezone.now().year:
            raise ValidationError(
                'Год выпуска произведения не может быть больше текущего!'
            )
