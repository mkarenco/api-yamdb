from django.utils import timezone
from rest_framework import serializers

from reviews import models


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    В поле genre обрабатывается список слагов жанров произведения.
    В поле category используется имя категории при отображении.
    Прописан метод валидации поля year: год выпуска произведения
    не позже текущего.
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
    """Сериализатор для модели Category."""

    class Meta:
        model = models.Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = models.Genre
        fields = '__all__'
