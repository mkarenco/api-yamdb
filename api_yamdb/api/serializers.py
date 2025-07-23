from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews import constants, models
from .mixins import UsernameValidationMixin

User = get_user_model()


class RegisterUserSerializer(serializers.Serializer, UsernameValidationMixin):

    email = serializers.EmailField(
        max_length=constants.EMAIL_LENGTH,
        required=True
    )
    username = serializers.CharField(
        max_length=constants.USERNAME_LENGTH,
        required=True
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username and email:
            username_exists = User.objects.filter(username=username).exists()
            email_exists = User.objects.filter(email=email).exists()

            if username_exists and email_exists:
                if not User.objects.filter(username=username,
                                           email=email
                                           ).exists():
                    raise serializers.ValidationError({
                        'username': ('Пользователь с таким username'
                                     'уже существует.'),
                        'email': 'Пользователь с таким email уже существует.'
                    })
            elif username_exists:
                raise serializers.ValidationError({
                    'username': 'Пользователь с таким username уже существует.'
                })
            elif email_exists:
                raise serializers.ValidationError({
                    'email': 'Пользователь с таким email уже существует.'
                })
        return data


class UserSerializer(serializers.ModelSerializer, UsernameValidationMixin):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class TokenObtainSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=constants.USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=settings.CODE_LENGTH,
        required=True
    )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):

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

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context['view'].kwargs['title_id']

        if request and request.method == 'POST':
            if models.Review.objects.filter(
                title_id=title_id, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date')
