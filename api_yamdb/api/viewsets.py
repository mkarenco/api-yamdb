from rest_framework import mixins, viewsets


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет, обеспечивающий выполнение методов 'create', 'list' и 'destroy'.
    Создание и удаление объекта, получение всех объектов модели.
    При использовании необходимо переопределить атрибуты 'queryset'
    и 'serializer_class'.
    """
    pass
