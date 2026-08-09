import os
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()

DEMO_PASSWORD = 'FoodgramDemo2026!'
DEMO_USERS = (
    {
        'email': 'chef.one@foodgram.local',
        'username': 'chef_one',
        'first_name': 'Анна',
        'last_name': 'Поварова',
    },
    {
        'email': 'chef.two@foodgram.local',
        'username': 'chef_two',
        'first_name': 'Иван',
        'last_name': 'Кулинаров',
    },
)
DEMO_RECIPES = (
    {
        'email': 'chef.one@foodgram.local',
        'name': 'Быстрый завтрак Foodgram',
        'text': 'Простой демонстрационный рецепт для проверки проекта.',
        'cooking_time': 10,
        'slug': 'breakfast',
        'color': (244, 190, 91),
    },
    {
        'email': 'chef.two@foodgram.local',
        'name': 'Домашний обед Foodgram',
        'text': 'Тестовый рецепт для демонстрации списка рецептов.',
        'cooking_time': 25,
        'slug': 'lunch',
        'color': (120, 176, 122),
    },
)


def build_image(name, color):
    buffer = BytesIO()
    Image.new('RGB', (800, 600), color=color).save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue(), name=name)


class Command(BaseCommand):
    help = 'Создаёт демонстрационных пользователей и рецепты.'

    @transaction.atomic
    def handle(self, *args, **options):
        ingredients = list(Ingredient.objects.all()[:3])
        tags = {tag.slug: tag for tag in Tag.objects.all()}
        if len(ingredients) < 2 or not tags:
            self.stdout.write(
                self.style.WARNING(
                    'Недостаточно ингредиентов или тегов для демо-данных.'
                )
            )
            return

        users = {}
        for payload in DEMO_USERS:
            user, created = User.objects.get_or_create(
                email=payload['email'],
                defaults={
                    'username': payload['username'],
                    'first_name': payload['first_name'],
                    'last_name': payload['last_name'],
                },
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save(update_fields=('password',))
            users[user.email] = user

        admin_password = os.getenv('FOODGRAM_ADMIN_PASSWORD')
        admin_email = os.getenv(
            'FOODGRAM_ADMIN_EMAIL',
            'admin@foodgram.local',
        )
        if admin_password:
            admin, _ = User.objects.get_or_create(
                email=admin_email,
                defaults={
                    'username': os.getenv(
                        'FOODGRAM_ADMIN_USERNAME',
                        'foodgram_admin',
                    ),
                    'first_name': 'Foodgram',
                    'last_name': 'Admin',
                },
            )
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.set_password(admin_password)
            admin.save()
            users[admin.email] = admin

        recipes = list(DEMO_RECIPES)
        if admin_password:
            recipes.append(
                {
                    'email': admin_email,
                    'name': 'Рецепт администратора Foodgram',
                    'text': (
                        'Демонстрационный рецепт пользователя '
                        'с правами администратора.'
                    ),
                    'cooking_time': 15,
                    'slug': 'dinner',
                    'color': (132, 146, 201),
                }
            )

        created_recipes = 0
        for index, payload in enumerate(recipes, start=1):
            user = users.get(payload['email'])
            tag = tags.get(payload['slug']) or next(iter(tags.values()))
            if user is None:
                continue
            if Recipe.objects.filter(
                author=user,
                name=payload['name'],
            ).exists():
                continue

            recipe = Recipe(
                author=user,
                name=payload['name'],
                text=payload['text'],
                cooking_time=payload['cooking_time'],
            )
            recipe.image.save(
                f'demo-{index}.jpg',
                build_image(f'demo-{index}.jpg', payload['color']),
                save=False,
            )
            recipe.save()
            recipe.tags.add(tag)
            RecipeIngredient.objects.bulk_create(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=(position + 1) * 50,
                )
                for position, ingredient in enumerate(ingredients)
            )
            created_recipes += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Демо-данные готовы. '
                f'Новых рецептов: {created_recipes}.'
            )
        )
