from rest_framework import serializers

from reviews import models


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

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
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = models.Genre
        fields = ('id', 'name', 'slug')
