from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews import models

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Позволяет создавать и отображать категории произведений."""

    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """
    Позволяет создавать и отображать жанры произведений.
    """

    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Позволяет отображать произведения.
    Для категории и жанров указывается slug.
    """

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Позволяет создавать произведения.
    Для категории и жанров указывается slug.
    """

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Genre.objects.all(),
        many=True,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all()
    )

    class Meta:
        model = models.Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitleReadSerializer(instance, context=self.context).data

    def validate_year(self, year):
        if models.is_year_lte_now(year):
            return year


class ReviewSerializer(serializers.ModelSerializer):
    """Позволяет создавать и отображать обзоры."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')

        if request and request.method == 'POST':
            if models.Review.objects.filter(
                title_id=title_id, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Позволяет создавать и отображать комментарии к обзорам.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date')
