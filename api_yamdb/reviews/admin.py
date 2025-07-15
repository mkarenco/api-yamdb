from django.contrib import admin

from . import models


class DivisionAttributeAdmin(admin.ModelAdmin):
    """
    Общий класс для для настройки админ-зоны
    модели-свойства объекта (внешнего ключа).
    """

    list_display = (
        'name',
        'slug'
    )
    search_fields = (
        'name',
    )
    list_display_links = (
        'name',
    )
    ordering = (
        'name',
    )


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

    list_display = (
        'name',
        'year',
        'description',
        'category',
        'rating'
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'year',
        'category',
        'rating'
    )
    list_display_links = (
        'name',
    )
    ordering = (
        'name', '-year', '-rating'
    )
    empty_value_display = '-пусто-'


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Review."""

    list_display = (
        'author',
        'text',
        'score',
        'pub_date',
    )
    search_fields = (
        'author',
        'text'
    )
    list_filter = (
        'author',
        'score',
        'pub_date',
    )
    ordering = (
        '-pub_date', 'author', '-score'
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Comment."""

    list_display = (
        'author',
        'text',
        'pub_date',
    )
    search_fields = (
        'author',
        'text'
    )
    list_filter = (
        'author',
        'pub_date',
    )
    ordering = (
        '-pub_date', 'author'
    )
