from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DivisionAttributeModel(models.Model):
    """
    Абстрактная модель.
    Содержит поля: имени и уникальный слаг.
    """

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:50]


class AbstractFeedback(models.Model):
    """
    Абстрактная модель.
    Содержит поля: текста и даты создания
    """

    text = models.TextField()
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text[:30]
