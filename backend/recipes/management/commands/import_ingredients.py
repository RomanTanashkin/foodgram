import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из data/ingredients.json.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default=None,
            help='Путь к JSON-файлу с ингредиентами.',
        )

    def handle(self, *args, **options):
        path = options['path']
        source = (
            Path(path)
            if path
            else settings.BASE_DIR.parent / 'data' / 'ingredients.json'
        )
        if not source.exists():
            raise CommandError(f'Файл не найден: {source}')

        try:
            with source.open(encoding='utf-8') as file:
                ingredients = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            raise CommandError(
                f'Не удалось прочитать {source}: {exc}'
            ) from exc

        before_count = Ingredient.objects.count()
        Ingredient.objects.bulk_create(
            (
                Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit'],
                )
                for item in ingredients
            ),
            ignore_conflicts=True,
        )
        created = Ingredient.objects.count() - before_count

        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт завершён. Добавлено ингредиентов: {created}.'
            )
        )
