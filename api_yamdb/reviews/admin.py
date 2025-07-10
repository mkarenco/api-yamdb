from django.contrib import admin

from .models import Category, Genre, Title


class AttributeAdmin(admin.ModelAdmin):
    """
    Общий класс для для настройки админ-зоны
    модели-свойства объекта (внешнего ключа).
    """

    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(AttributeAdmin):
    """Настройка админ-зоны для модели Category."""
    pass


@admin.register(Genre)
class GenreAdmin(AttributeAdmin):
    """Настройка админ-зоны для модели Genre."""
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка админ-зоны для модели Title."""

    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'description')
    list_filter = ('year', 'category')
    empty_value_display = '-пусто-'
