from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class DivisionAttributeAdmin(admin.ModelAdmin):
    """
    Общий класс для настройки админ-зоны
    модели-свойства объекта (внешнего ключа).
    """

    list_display = (
        'name',
        'slug'
    )
    search_fields = (
        'name',
        'slug'
    )
    list_filter = (
        'name',
        'slug',
    )
    ordering = (
        'name',
    )


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active'
    )
    list_editable = (
        'email',
        'role'
    )
    search_fields = (
        'username',
        'email'
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff'
    )
    ordering = (
        'username',
    )


@admin.register(models.Category)
class CategoryAdmin(DivisionAttributeAdmin):
    """Настройка админ-зоны для модели Category."""


@admin.register(models.Genre)
class GenreAdmin(DivisionAttributeAdmin):
    """Настройка админ-зоны для модели Genre."""


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Title."""

    list_display = (
        'name',
        'year',
        'category',
        'description'
    )
    list_editable = (
        'year',
        'description',
    )
    search_fields = (
        'name',
        'description',
    )
    list_filter = (
        'year',
    )
    ordering = (
        'name',
        '-year'
    )
    empty_value_display = '-пусто-'


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Review."""

    list_display = (
        'author',
        'score',
        'text',
        'pub_date',
    )
    list_editable = (
        'text',
        'score'
    )
    search_fields = (
        'author',
        'text',
        'title'
    )
    list_filter = (
        'author',
        'score',
        'pub_date',
    )
    ordering = (
        '-pub_date',
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Comment."""

    list_display = (
        'author',
        'text',
        'pub_date',
    )
    list_editable = (
        'text',
    )
    search_fields = (
        'author',
        'text',
    )
    list_filter = (
        'author',
        'pub_date',
    )
    ordering = (
        '-pub_date',
    )
