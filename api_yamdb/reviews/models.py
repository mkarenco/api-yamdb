from datetime import datetime

from django.db import models
from django.db.models import CheckConstraint, Q


class Category(models.Model):
    """Модель объекта категории произведения."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель объекта категории произведения."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель объекта произведения."""

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
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(year__lte=datetime.now().year),
                name='year_now_or_earlier'
            )
        ]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
