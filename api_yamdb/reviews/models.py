from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class DivisionAttributeModel(models.Model):
    """
    Абстрактная модель свойства объекта.
    Содержит поля имени признака деления на группы и уникальный слаг.
    Описывает строковое отображение объекта.
    """

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:50]


class Category(DivisionAttributeModel):
    """Модель объекта категории произведения."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(DivisionAttributeModel):
    """Модель объекта категории произведения."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Модель объекта произведения (фильма, книги и т.п.).
    Объект модели может иметь несколько жанров и только одну категорию.
    Нельзя добавить произведение с годом выпуска в будущем.
    К проиведнию моно написать обзор (комментарий).
    """

    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    rating = models.IntegerField('Рейтинг', default=None)
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
        return self.name[:50]

    def clean(self):
        if self.year > timezone.now().year:
            raise ValidationError(
                'Год выпуска произведения не может быть больше текущего!'
            )


class Reviews(models.Model):
    """
    Модель обзора к произведению (Модели Title).
    Содержит автора, текст, ссылку на тайтл и дату создания.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ('-created', 'author')

    def __str__(self):
        return self.text[:30]
