from django.db.models import Avg


def update_rating(title):
    """
    Обновляет рейтинг произведения на основе средней оценки всех отзывов.

    Вычисляет среднее значение поля score у связанных отзывов модели Title.
    Округляет его до ближайшего целого числа и сохраняет в поле rating.
    Если у произведения нет отзывов, устанавливает rating в None.
    """
    avg = title.reviews.aggregate(Avg('score'))['score__avg']
    if avg is not None:
        title.rating = round(avg)
    else:
        title.rating = None
    title.save()
