# Foodgram

Recipe-sharing web application. Users publish recipes, subscribe to authors, keep a favourites list and a shopping cart, and download the aggregated shopping list as a file.

Built during the *Python Developer* course at Yandex Practicum (2025–2026). Every project was reviewed and accepted by a course mentor.

## Features

- Recipes with tags, ingredients, images and cooking time
- Subscriptions to authors, favourites, shopping cart
- Shopping list export (ingredients summed across selected recipes)
- Token authentication and user management (Djoser)
- Admin panel with search and filters
- Full REST API with OpenAPI documentation at `/api/docs/`

## Tech stack

Python 3.12 · Django · Django REST Framework · Djoser · PostgreSQL · Gunicorn · Nginx · Docker Compose · GitHub Actions · React (frontend from the course starter kit)

## API overview

All endpoints live under `/api/`: `users`, `tags`, `ingredients`, `recipes`, plus `recipes/<id>/favorite/`, `recipes/<id>/shopping_cart/`, `recipes/<id>/get-link/`, `recipes/download_shopping_cart/`, `users/subscriptions/`, `users/me/avatar/`.

## Run locally (backend only)

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py import_ingredients
python backend/manage.py seed_tags
python backend/manage.py runserver
```

## Run the full stack with Docker

```bash
cp infra/.env.example infra/.env
docker compose -f infra/docker-compose.yml up -d --build
```

The app is served at `http://localhost`, the API docs at `http://localhost/api/docs/`. On first start the backend container applies migrations, collects static files, imports ingredients, creates base tags and seeds demo data (demo credentials are defined in `backend/recipes/management/commands/seed_demo_data.py`).

## Quality checks

The official Postman collection (`postman_collection/`) runs in CI together with Django system checks, migration checks and flake8:

```bash
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
flake8 backend --config=setup.cfg
npx newman run postman_collection/foodgram.postman_collection.json --env-var baseUrl=http://127.0.0.1:8000
```

## CI/CD

`.github/workflows/main.yml`:

1. On every push to `main` — Django checks, migrations check, Postman collection, tests, flake8.
2. On manual run (`workflow_dispatch`) — build and push backend/frontend images to Docker Hub, copy `docker-compose.production.yml` to the server via SSH and restart the containers.

Production uses three long-running containers: PostgreSQL, Django + Gunicorn, Nginx. Required GitHub secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `HOST`, `USER`, `SSH_KEY`, `SSH_PASSPHRASE`.

## Author

Roman Tanashkin — [github.com/RomanTanashkin](https://github.com/RomanTanashkin)
