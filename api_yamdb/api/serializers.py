from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews import models


class TitleSerializer(serializers.ModelSerializer):
    """
    Позволяет создавать и отображать произведения,
    указывая жанры (по слагам) и категорию (по имени).
    """

    genre = serializers.SlugRelatedField(
        queryset=models.Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.Category.objects.all()
    )

    class Meta:
        model = models.Title
        fields = '__all__'
        read_only_fields = ('rating',)

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение с годом выпуска больше текущего!'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Позволяет создавать и отображать категории произведений."""

    class Meta:
        model = models.Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Позволяет создавать и отображать жанры произведений.
    """

    class Meta:
        model = models.Genre
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    """Позволяет создавать и отображать жанры обзоры."""

    author = SlugRelatedField(  # Показывает вместо ID автора его username
        slug_field='username'
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    class Meta:
        fields = '__all__'
        model = models.Reviews
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=models.Reviews.objects.all(),
                fields=['author', 'title'],
                message='Вы уже оставили отзыв на это произведение.'
            )
        ]
