from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DivisionAttributeModel(models.Model):
    """
    Абстрактная модель.
    Содержит поля: имени и уникальный слаг.
    """

    name = models.CharField(
        'Название',
        max_length=256,
        help_text='Введите название категории (например, "Фильмы", "Книги").'
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=50,
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
    Содержит поля: текста и даты создания
    """

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

    def __str__(self):
        return self.text[:30]
