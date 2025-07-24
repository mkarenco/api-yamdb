# YaMDb

**YaMDb** — API для работы с произведениями искусства (фильмы, книги, музыка и т.п.), отзывами, комментариями и пользовательскими рейтингами
___

## Возможности:

+  Регистрация пользователей

+ Аутентификация по JWT

+ CRUD для произведений, жанров, категорий

+ Оставление отзывов и комментариев

+ Система рейтинга на основе отзывов

+ Роли пользователей: **user / moderator / admin**
___

## Стек технологий

+ Python

+ Django

+ Django REST Framework

+ SimpleJWT
___

## Установка и запуск проекта

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/api-yamdb.git
cd api-yamdb
```

2. **Создайте виртуальное окружение и активируйте его:**

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Примените миграции:**

```bash
python manage.py migrate
```

5. **Создайте суперпользователя (по желанию):**

```bash
python manage.py createsuperuser
```

6. **Запустите проект:**

```bash
python manage.py runserver
```
___

## Импорт данных из CSV

Для загрузки данных в базу из CSV-файлов используется специальная команда:

```python
python manage.py import_csv
```
___

## Примеры запросов

| Метод | URL                               | Описание                         |
|-------|-----------------------------------|----------------------------------|
| POST  | /api/v1/auth/signup/              | Регистрация пользователя         |
| POST  | /api/v1/auth/token/               | Получение JWT-токена              |
| GET   | /api/v1/titles/                   | Получение списка всех произведений|
| POST  | /api/v1/titles/                   | Добавление произведения             |
| GET   | /api/v1/titles/{id}/              | Детальная информация о произведении |
| GET   | api/v1/titles/{title_id}/reviews/ | Получение списка всех отзывов |
| GET   | api/v1/titles/{title_id}/reviews/{review_id}/| Полуение отзыва по id |
___

## Структура проекта

```bash
api_yamdb/
├── api/
├── api_yamdb/
├── reviews/
├── static/
├── templates/
├── users/
└── manage.py
```
___

## Авторы

+ [*Миша Макаренко*](https://github.com/mkarenco)
+ [*Ольга Ушакова*](https://github.com/Olga-Ushakova)
+ [*Ярослав Мищенко*](https://github.com/5pix)

