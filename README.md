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
poetry run python manage.py runserver

# Создание суперпользователя
```commandline
poetry run python manage.py create_admin
```

# Запуск планировщика
```commandline
poetry run python manage.py runscheduler
```

# Требования к окружению
Python 3.8+

Django 3.2+

APScheduler 3.7+

Poetry

Redis (для Celery)