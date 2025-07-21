from django.conf import settings
from django.db import models


class DivisionAttributeModel(models.Model):
    """
    Абстрактная модель.
    Содержит поля: имени и уникальный слаг.
    """

    name = models.CharField(
        'Название',
        max_length=settings.NAME_LENGTH,
        help_text='Введите название категории (например, "Фильмы", "Книги").'
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.SLUG_LENGTH,
        help_text='Укажите уникальный slug для категории (используется в URL).'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:50]


class AbstractFeedback(models.Model):
    """
    Абстрактная модель.
    Содержит поля: текста и даты создания.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='Выберите автора обзора.'
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст обзора.'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        help_text='Дата публикации обзора (заполняется автоматически).'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]
