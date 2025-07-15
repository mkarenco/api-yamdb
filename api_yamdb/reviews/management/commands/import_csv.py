import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.shortcuts import get_object_or_404

from reviews import models

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузка данных в модели из csv-файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='static/data/',
            help='Путь до csv-файлов'
        )

    @transaction.atomic
    def handle(self, args, *options):
        base_path = options['path']
        self.load_categories(f'{base_path}category.csv')
        self.load_genres(f'{base_path}genre.csv')
        self.load_users(f'{base_path}users.csv')
        self.load_titles(f'{base_path}titles.csv')
        self.load_genre_title(f'{base_path}genre_title.csv')
        self.load_reviews(f'{base_path}review.csv')
        self.load_comments(f'{base_path}comments.csv')

    def load_categories(self, file_path):
        self.stdout.write(f'Загрузка категорий из {file_path}.')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                models.Category.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Категории загружены.'))

    def load_genres(self, file_path):
        self.stdout.write(f'Загрузка жанров из {file_path}.')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                models.Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Жанры загружены.'))

    def load_users(self, file_path):
        self.stdout.write(f'Загрузка пользователей из {file_path}.')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row['bio'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Пользователи загружены.'))

    def load_genre_title(self, file_path):
        self.stdout.write(
            f'Загрузка связей произведений и жанров из {file_path}.'
        )
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                models.Title_Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'title_id': row['title_id'],
                        'genre_id': row['genre_id']
                    }
                )
        self.stdout.write(
            self.style.SUCCESS('Связи произведений и жанров загружены.')
        )

    def load_titles(self, file_path):
        self.stdout.write(f'Загрузка произведений из {file_path}.')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = get_object_or_404(
                    models.Category,
                    id=row['category']
                )
                relations = models.Title_Genre.objects.filter(
                    title_id=row['id']
                )
                genres = models.Genre.objects.filter(title_genre__in=relations)
                models.Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'category': category,
                        'genre': genres
                    }
                )
        self.stdout.write(self.style.SUCCESS('Произведения загружены.'))

    def load_reviews(self, file_path):
        self.stdout.write(f'Загрузка отзывов из {file_path}.')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = get_object_or_404(models.Title, id=row['title_id'])
                author = get_object_or_404(User, id=row['author'])
                models.Review.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'title': title,
                        'text': row['text'],
                        'author': author,
                        'score': row['score'],
                        'pub_date': row['pub_date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Отзывы загружены.'))

    def load_comments(self, file_path):
        self.stdout.write(f'Загрузка комметариев к отзывам из {file_path}.')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                author = get_object_or_404(User, id=row['author'])
                review = get_object_or_404(models.Review, id=row['review_id'])
                models.Comment.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'author': author,
                        'review': review,
                        'text': row['text'],
                        'pub_date': row['pub_date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Комментарии загружены.'))
