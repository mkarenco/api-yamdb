from reviews.validators import validate_username_symbols


class UsernameValidationMixin:
    """
    Миксин для валидации поля `username`.
    Проверяет:
    - имя не совпадает с USER_SELF_PAGE
    - содержит только допустимые символы
    """

    def validate_username(self, username):
        return validate_username_symbols(username)
