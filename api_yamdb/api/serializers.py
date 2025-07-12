from django.utils import timezone
from rest_framework import serializers

from reviews import models


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
