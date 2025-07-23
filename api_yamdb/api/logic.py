from random import choices

from django.core.mail import send_mail

from api_yamdb.settings import CODE_LENGTH, CODE_SYMBOLS, DEFAULT_FROM_EMAIL


def _confirmation_code():
    """генерация кода подтверждения."""

    return ''.join(choices(CODE_SYMBOLS, k=CODE_LENGTH))


def _send_confirmation_email(email, confirmation_code):
    """Отправляет код подтверждения на указанный email при регистрации."""

    send_mail(
        'Код подтверждения для регистрации',
        f'Ваш код подтверждения: {confirmation_code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
