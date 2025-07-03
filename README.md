# Django Project with APScheduler 
## Описание проекта
Данный учебный проект — это веб-приложение, которое содержит возможность публиковать 
и управлять продуктами, вести блог, создавать и управлять рассылками.

## Установка
1. Клонирование репозитория:

```commandline

git clone https://github.com/Chocoeater/DjangoProject.git
cd DjangoProject
```

2. Установка Poetry (если еще не установлен):

```commandline

curl -sSL https://install.python-poetry.org | python3 -
```
3. Создание и активация виртуального окружения:

```commandline
poetry shell
```
4. Установка зависимостей:

```commandline
poetry install
```
## Настройка
Настройка базы данных в settings.py:

В проекте используется postgresql
Для настройки подключения к БД заполните необходимые параметры в .env по шаблону .env.example

## Запуск миграций:

```commandline
poetry run python manage.py migrate
```

# Запуск сервера разработки

**ВАЖНО! Перед запуском сервера необходимо запустить сервер Redis!**
```commandline
poetry run python manage.py runserver
```

# Создание тестовых пользователей


```commandline
poetry run python manage.py create_admin
```

Остальных пользователей можно создать либо через функционал регистрации с последующей выдачей необходимый прав,
если потребуется, либо при помощи загрузки готовых фикстур (для теста):

```commandline
python manage.py loaddata group_fixture.json
python manage.py loaddata users_fixture.json
```

Также существуют другие фикстуры, которые можно найти в корне проекта.

# Запуск планировщика
Осуществляется через кастомную команду:

```commandline
poetry run python manage.py runapscheduler
```

# Требования к окружению
Python 3.8+

Django 3.2+

APScheduler 3.7+

Poetry

Redis (для Celery)