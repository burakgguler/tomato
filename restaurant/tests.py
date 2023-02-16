import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from restaurant.models import Restaurant

login_url = reverse("token_obtain_pair")
user_data = {
    "username": "burak_res",
    "password": "pass123"
}
restaurant_data = {
    "name": "Res Test Case",
    "cuisine": "test case cuisine",
    "location": "test case location",
    "slug": "test-case-restaurant"
}


class RestaurantCreateListTestCase(APITestCase):
    create_url = reverse("restaurant:create")
    list_url = reverse("restaurant:list")

    def setUp(self):
        self.user = User.objects.create_user(username=user_data["username"], password=user_data["password"])
        self.test_authentication()

    def test_authentication(self):
        response = self.client.post(login_url, data=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in json.loads(response.content))
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_restaurant(self):
        response = self.client.post(self.create_url, restaurant_data)
        self.assertEqual(response.status_code, 201)

    def test_create_restaurant_unauthorized(self):
        self.client.credentials()
        response = self.client.post(self.create_url, restaurant_data)
        self.assertEqual(response.status_code, 401)

    def test_list_restaurants(self):
        self.test_create_restaurant()
        response = self.client.get(self.list_url)
        response_list = len(json.loads(response.content)["results"])
        created_restaurants = Restaurant.objects.all().count()
        self.assertTrue(response_list == created_restaurants)


class RestaurantUpdateDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=user_data["username"], password=user_data["password"])
        self.another_user = User.objects.create_user(username="another_burak", password=user_data["password"])
        self.restaurant = Restaurant.objects.create(
            name=restaurant_data["name"],
            location=restaurant_data["location"],
            cuisine=restaurant_data["cuisine"],
            slug=restaurant_data["slug"]
        )
        self.update_url = reverse("restaurant:update", kwargs={"slug": self.restaurant.slug})
        self.detail_url = reverse("restaurant:detail", kwargs={"slug": self.restaurant.slug})
        self.test_authentication()

    def test_authentication(self, username=user_data["username"], password=user_data["password"]):
        response = self.client.post(login_url, data={"username": username, "password": password})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in json.loads(response.content))
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_restaurant_delete(self):
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, 204)

    def test_restaurant_delete_another_user(self):
        self.test_authentication("another_burak")
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, 403)

    def test_restaurant_update(self):
        data = {
            "cuisine": "updated cuisine",
            "location": "updated location"
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Restaurant.objects.get(id=self.restaurant.id).cuisine == data["cuisine"])

    def test_restaurant_update_another_user(self):
        self.test_authentication("another_burak")
        data = {
            "cuisine": "updated cuisine",
            "location": "updated location"
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Restaurant.objects.get(id=self.restaurant.id).location == data["location"])

    def test_restaurant_update_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 401)

    def test_restaurant_get_detail_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
