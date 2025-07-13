import secrets

from django.core.mail import send_mail

from api_yamdb import settings


@staticmethod
def _assign_confirmation_code():
    """
    генерация кода подтверждения для вновь зарегистрированного
    """
    return ''.join(secrets.choice('0123456789ABCDEFG') for _ in range(6))


@staticmethod
def _send_confirmation_email(email, confirmation_code):
    """
    Отправляет код подтверждения на указанный email при регистрации
    """
    send_mail(
        'Код подтверждения для регистрации',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
