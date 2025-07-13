from rest_framework import mixins, viewsets


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Базовый абстрактный ViewSet для операций:
    - получения списка объектов (list),
    - создания нового объекта (create),
    - удаления объекта (destroy).
    """

    pass
