from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Основной класс по работе с моделью User и обработки кастомных полей
    """
    pass


# Все что выше перенести в приложение users

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(  # Показывает вместо ID автора его username
        read_only=True,
        slug_field='username'
    )
    # сделать score в ветки для оценки

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=['author', 'title'],
                message='Вы уже оставили отзыв на это произведение.'
            )
        ]
