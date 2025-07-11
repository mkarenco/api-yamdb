from django.contrib import admin

from . import models


class DivisionAttributeAdmin(admin.ModelAdmin):
    """
    Общий класс для для настройки админ-зоны
    модели-свойства объекта (внешнего ключа).
    """

    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(models.Category)
class CategoryAdmin(DivisionAttributeAdmin):
    """Настройка админ-зоны для модели Category."""
    pass


@admin.register(models.Genre)
class GenreAdmin(DivisionAttributeAdmin):
    """Настройка админ-зоны для модели Genre."""
    pass


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Title."""

    list_display = ('name', 'year', 'description', 'category', 'rating')
    search_fields = ('name', 'description')
    list_filter = ('year', 'category')
    empty_value_display = '-пусто-'
