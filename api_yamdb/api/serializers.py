from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews import models

User = get_user_model()


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
        slug_field='slug',
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


class ReviewSerializer(serializers.ModelSerializer):
    """Позволяет создавать и отображать жанры обзоры."""

    author = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    class Meta:
        fields = '__all__'
        model = models.Review
        validators = [
            UniqueTogetherValidator(
                queryset=models.Review.objects.all(),
                fields=['author', 'title'],
                message='Вы уже оставили отзыв на это произведение.'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Позволяет создавать и отображать комментарии к обзорам.
    """

    author = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = models.Comment
        fields = '__all__'
