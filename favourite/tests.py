from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from favourite.models import Favourite
from restaurant.models import Restaurant

login_url = reverse("token_obtain_pair")


class FavouriteCreateListTestCase(APITestCase):
    favourite_url = reverse("favourite:list-create")

    def setUp(self):
        self.data = {
            "username": "burak_fav",
            "password": "test1234"
        }
        self.restaurant = Restaurant.objects.create(name="Fav", location="a", cuisine="b", slug="fav-test")
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])
        self.test_authentication()

    def test_authentication(self):
        response = self.client.post(login_url, self.data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_add_favourite(self):
        data = {
            "content": "fav testing",
            "user": self.user.id,
            "restaurant": self.restaurant.id
        }
        response = self.client.post(self.favourite_url, data)
        self.assertEqual(201, response.status_code)

    def test_list_favourites(self):
        self.test_add_favourite()
        response = self.client.get(self.favourite_url)
        result_count = len(response.json()["results"])
        test_user_fav_count = Favourite.objects.filter(user=self.user).count()
        self.assertTrue(result_count == test_user_fav_count)
