# Foodgram

Foodgram — веб-приложение для публикации рецептов. Пользователи могут создавать рецепты, подписываться на авторов, добавлять рецепты в избранное и список покупок, а затем скачивать агрегированный список ингредиентов.

## Стек

- Python 3.12, Django, Django REST Framework, Djoser
- PostgreSQL
- Gunicorn
- Nginx
- Docker Compose
- React (готовый SPA из стартового проекта)
- GitHub Actions

## API

После запуска проекта спецификация доступна по адресу:

```text
http://localhost/api/docs/
```

Основные API-ресурсы находятся под префиксом `/api/`.

## Локальный запуск backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py import_ingredients
python backend/manage.py seed_tags
python backend/manage.py runserver
```

В Windows активировать окружение можно командой:

```powershell
venv\Scripts\activate
```

## Локальный запуск всего проекта в Docker

Создайте локальный файл окружения:

```bash
cp infra/.env.example infra/.env
```

Затем запустите:

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

Приложение будет доступно по адресу `http://localhost`, а документация API — `http://localhost/api/docs/`.

При первом старте backend автоматически выполняет миграции, собирает Django static, импортирует исходный список ингредиентов, создаёт базовые теги и демонстрационные данные.

## Проверка API

В репозитории находится официальная Postman-коллекция задания:

```text
postman_collection/foodgram.postman_collection.json
```

Она автоматически запускается в GitHub Actions вместе с Django checks, тестами и flake8.

## Production

Для production используется `docker-compose.production.yml`. После завершения сборочного контейнера frontend постоянно работают три контейнера: PostgreSQL, Django + Gunicorn и Nginx.

Перед первым деплоем на сервере необходимо создать `~/foodgram/.env` по образцу `infra/.env.production.example`.

CI/CD при пуше в `main`:

1. проверяет Django-проект и миграции;
2. запускает официальную Postman-коллекцию и тесты;
3. проверяет PEP 8;
4. собирает и публикует backend/frontend образы в Docker Hub;
5. копирует production-конфигурацию на сервер;
6. обновляет контейнеры и конфигурацию системного Nginx.

Для GitHub Actions используются секреты `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `HOST`, `USER`, `SSH_KEY`, `SSH_PASSPHRASE`.

Адрес production-сервера будет указан здесь после первого успешного деплоя.
