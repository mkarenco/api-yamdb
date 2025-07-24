from reviews.validators import validate_reserved_username


class UsernameValidationMixin:
    """
    Миксин для валидации поля `username`.
    Проверяет:
    - имя не совпадает с USER_SELF_PAGE
    - содержит только допустимые символы
    """

    def validate_username(self, username):
        return validate_reserved_username(username)
