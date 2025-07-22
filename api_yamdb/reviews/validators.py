import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework.exceptions import ValidationError as DRFValidationError

USER_SELF_PAGE = 'me'


def is_year_lte_now(year):
    """
    Метод валидации года выпуска произведения.
    Год не может быть больше текущего.
    """

    if year > timezone.now().year:
        raise DjangoValidationError(
            'Нельзя добавить произведение с годом выпуска в будущем.'
            f'Указанный год выпуска {year}.'
        )

    return year


def validate_reserved_username(username, raise_type='drf'):
    """
    Проверяет:
    - username не совпадает с USER_SELF_PAGE
    - состоит только из допустимых символов
    """

    if username == USER_SELF_PAGE:
        return _raise_validation_error(
            f'Использовать имя {USER_SELF_PAGE} нельзя.',
            raise_type
        )

    if not re.fullmatch(r'^[\w.@+-]+\Z', username):
        return _raise_validation_error(
            'Имя пользователя содержит недопустимые символы.',
            raise_type
        )


def _raise_validation_error(message, raise_type):
    if raise_type == 'drf':
        raise DRFValidationError(message)
    raise DjangoValidationError(message)
