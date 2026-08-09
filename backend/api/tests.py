from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Ingredient, Tag

User = get_user_model()


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        payload = {
            'email': 'user@example.com',
            'username': 'food_user',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password': 'StrongPass123!',
        }
        response = self.client.post('/api/users/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            set(response.data),
            {'id', 'email', 'username', 'first_name', 'last_name'},
        )
        self.assertNotIn('password', response.data)
        self.assertTrue(
            User.objects.get(email=payload['email']).check_password(
                payload['password']
            )
        )


class IngredientApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Ingredient.objects.create(name='Картофель', measurement_unit='г')
        Ingredient.objects.create(name='Капуста', measurement_unit='г')

    def test_ingredient_search_is_case_insensitive_prefix(self):
        response = self.client.get('/api/ingredients/', {'name': 'КАР'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Картофель')


class TagApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Tag.objects.create(name='Завтрак', slug='breakfast')

    def test_tags_are_public(self):
        response = self.client.get('/api/tags/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['slug'], 'breakfast')
