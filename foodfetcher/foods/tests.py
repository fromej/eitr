from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import FavoriteFoods

User = get_user_model()

# Create your tests here.

class VeggiesEndpointTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="eitr_test",
            password="test_password"
        )

        FavoriteFoods.objects.create(foods='Spinach', veggy=True)
        FavoriteFoods.objects.create(foods='Tofu', veggy=True)
        FavoriteFoods.objects.create(foods='Chicken', veggy=False)
        FavoriteFoods.objects.create(foods='Lentils', veggy=True)

        self.url = reverse("veggies")

    def test_veggy_list(self):
        self.client.login(
            username="eitr_test",
            password="test_password"
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["total"], 3)

    def test_login_required_for_veggy_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        