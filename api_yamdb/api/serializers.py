from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews import models
from reviews.models import Reviews


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Позволяет создавать и отображать произведения,
    указывая жанры (по слагам) и категорию (по имени).
    """

    genre = serializers.ListField(
        child=serializers.SlugField(),
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.Category.objects.all()
    )

    class Meta:
        model = models.Title
        fields = '__all__'

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение с годом выпуска больше текущего!'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    Позволяет создавать и отображать категории произведений.
    """

    class Meta:
        model = models.Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    Позволяет создавать и отображать жанры произведений.
    """

    class Meta:
        model = models.Genre
        fields = '__all__'

        
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Основной класс по работе с моделью User и обработки кастомных полей
    """
    pass


# Все что выше перенести в приложение users


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
