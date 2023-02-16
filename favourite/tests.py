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
        self.authentication()

    def authentication(self):
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


class FavouriteUpdateDeleteTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "burak_fav_list",
            "password": "test1234"
        }
        self.restaurant = Restaurant.objects.create(name="Fav", location="a", cuisine="b", slug="fav-test")
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])
        self.favourite = Favourite.objects.create(restaurant=self.restaurant, user=self.user)
        self.update_url = reverse("favourite:update-delete", kwargs={"pk": self.favourite.pk})
        self.authentication()

    def authentication(self):
        response = self.client.post(login_url, self.data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_favourite_delete(self):
        response = self.client.delete(self.update_url)
        self.assertEqual(204, response.status_code)

    def test_favourite_update(self):
        data = {
            "content": "updated content!",
            "restaurant": self.restaurant.id,
            "user": self.user.id
        }
        response = self.client.put(self.update_url, data)
        favourite_obj = Favourite.objects.get(id=self.favourite.id)
        self.assertEqual(200, response.status_code)
        self.assertTrue(favourite_obj.content == data["content"])
