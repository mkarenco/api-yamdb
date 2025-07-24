import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def is_year_lte_now(year):
    """
    Метод валидации года выпуска произведения.
    Год не может быть больше текущего.
    """

    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            'Нельзя добавить произведение с годом выпуска в будущем.'
            f'Указанный год выпуска {year} больше {current_year}.'
        )

    return year


def validate_username_symbols(username):
    """
    Проверяет:
    - username не совпадает с USER_SELF_PAGE
    - состоит только из допустимых символов
    """

    if username == settings.USER_SELF_PAGE:
        raise ValidationError(
            f'Использовать имя {settings.USER_SELF_PAGE} нельзя.'
        )

    invalid_chars = sorted(set(
        re.findall(r'[^\w.@+-]', username)
    ))
    if not invalid_chars:
        return username

    invalid_display = ', '.join(f'<{char}>' for char in invalid_chars)
    raise ValidationError(
        f'Имя пользователя содержит недопустимые символы: {invalid_display}'
    )
