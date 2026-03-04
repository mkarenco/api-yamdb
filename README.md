# YaMDb

**YaMDb** — API для работы с произведениями искусства (фильмы, книги, музыка и т.п.), отзывами, комментариями и пользовательскими рейтингами

## Возможности:
+  **Регистрация пользователей**
+ **Аутентификация по JWT**
+ **CRUD для произведений, жанров, категорий**
+ **Оставление отзывов и комментариев**
+ **Система рейтинга на основе отзывов**
+ **Роли пользователей: user / moderator / admin**

## Стек технологий
+ **Python**
+ **Django**
+ **Django REST Framework**
+ **SimpleJWT**

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

## Импорт данных из CSV

Для загрузки данных в базу из CSV-файлов используется специальная команда:
```python
python manage.py import_csv
```

## Авторы
[*Миша Макаренко*](https://github.com/mkarenco)  
[*Ольга Ушакова*](https://github.com/Olga-Ushakova)  
[*Ярослав Мищенко*](https://github.com/5pix)

