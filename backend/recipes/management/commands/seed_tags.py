from django.core.management.base import BaseCommand

from recipes.models import Tag


DEFAULT_TAGS = (
    ('Завтрак', 'breakfast'),
    ('Обед', 'lunch'),
    ('Ужин', 'dinner'),
    ('Десерт', 'dessert'),
)


class Command(BaseCommand):
    help = 'Создаёт базовые теги Foodgram, если их ещё нет.'

    def handle(self, *args, **options):
        created = 0
        for name, slug in DEFAULT_TAGS:
            _, was_created = Tag.objects.get_or_create(
                name=name,
                slug=slug,
            )
            created += int(was_created)
        self.stdout.write(
            self.style.SUCCESS(
                f'Теги готовы. Добавлено: {created}.'
            )
        )
