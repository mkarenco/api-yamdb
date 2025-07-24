import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def is_year_lte_now(year):
    """
    Метод валидации года выпуска произведения.
    Год не может быть больше текущего.
    """

    if year > timezone.now().year:
        raise ValidationError(
            'Нельзя добавить произведение с годом выпуска в будущем.'
            f'Указанный год выпуска {year}.'
        )

    return year


def validate_reserved_username(username):
    """
    Проверяет:
    - username не совпадает с USER_SELF_PAGE
    - состоит только из допустимых символов
    """

    if username == settings.USER_SELF_PAGE:
        raise ValidationError(
            f'Использовать имя {settings.USER_SELF_PAGE} нельзя.'
        )

    if settings.ALLOWED_USERNAME_PATTERN.fullmatch(username):
        return username

    invalid_chars = sorted(set(
        char for char in username
        if not re.fullmatch(r'[\w.@+-]', char)
    ))

    invalid_display = ', '.join(f'"{char}"' for char in invalid_chars)
    raise ValidationError(
        f'Имя пользователя содержит недопустимые символы: {invalid_display}'
    )
