import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """
    Определяет фильтры для модели Title.
    Фильтрует по:
    - названию произведения,
    - году выпуска,
    - слагу категории,
    - слагу жанра.
    """

    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
