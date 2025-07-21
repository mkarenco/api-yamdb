import re

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


def validate_reserved_username(username, raise_type='drf'):
    """
    Проверяет:
    - username не совпадает с USER_SELF_PAGE
    - состоит только из допустимых символов
    """

    if username == settings.USER_SELF_PAGE:
        return _raise_validation_error(
            f'Использовать имя {settings.USER_SELF_PAGE} нельзя',
            raise_type
        )

    if not re.fullmatch(r'^[\w.@+-]+\Z', username):
        return _raise_validation_error(
            'Имя пользователя содержит недопустимые символы',
            raise_type
        )


def _raise_validation_error(message, raise_type):
    if raise_type == 'drf':
        raise DRFValidationError(message)
    raise DjangoValidationError(message)
