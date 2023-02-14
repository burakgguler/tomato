import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

login_url = reverse("token_obtain_pair")


class UserRegistrationTestCase(APITestCase):
    register_url = reverse("account:register")

    def test_user_registration(self):
        data = {
            "username": "buraktestcase",
            "password": "buraktest123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password_registration(self):
        data = {
            "username": "buraktestcase",
            "password": "1"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(400, response.status_code)

    def test_user_username_exists_registration(self):
        self.test_user_registration()
        data = {
            "username": "buraktestcase",
            "password": "buraktest111"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):  # logged user with session should not register
        self.test_user_registration()
        self.client.login(username='buraktestcase', password='buraktest123')

        response = self.client.get(self.register_url)
        self.assertEqual(403, response.status_code)

    def test_user_token_authenticated_registration(self):  # logged user with token should not register
        self.test_user_registration()
        data = {
            "username": "buraktestcase",
            "password": "buraktest123"
        }
        token_response = self.client.post(login_url, data)
        self.assertEqual(200, token_response.status_code)
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.register_url)
        self.assertEqual(403, response.status_code)


class UserLoginTestCase(APITestCase):

    def setUp(self):
        self.data = {
            "username": "buraktestcase",
            "password": "buraktest123"
        }
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])

    def test_user_token(self):
        response = self.client.post(login_url, self.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_credentials(self):
        response = self.client.post(login_url, {"username": "burakkk", "password": "wrongtest"})
        self.assertEqual(401, response.status_code)

    def test_user_no_data(self):
        response = self.client.post(login_url, {"username": "", "password": ""})
        self.assertEqual(400, response.status_code)


class UserPasswordChangeTestCase(APITestCase):
    password_url = reverse("account:change-password")

    def setUp(self):
        self.data = {
            "username": "buraktestcase",
            "password": "buraktest123"
        }
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])

    def test_user_token(self):
        token_response = self.client.post(login_url, self.data)
        self.assertEqual(200, token_response.status_code)
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated_user(self):
        response = self.client.get(self.password_url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_credentials(self):
        self.test_user_token()
        data = {
            "old_password": "buraktest123",
            "new_password": "newpasstest123"
        }
        response = self.client.put(self.password_url, data)
        self.assertEqual(204, response.status_code)


class UserProfileUpdateTestCase(APITestCase):
    profile_url = reverse("account:me")

    def setUp(self):
        self.data = {
            "username": "buraktestcase",
            "password": "buraktest123"
        }
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])

    def test_user_token(self):
        token_response = self.client.post(login_url, self.data)
        self.assertEqual(200, token_response.status_code)
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated_user(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(401, response.status_code)

    """
    def test_user_no_data(self):
        self.test_user_token()
        data = {
            "id": "",
            "first_name": "",
            "last_name": "",
            "profile": {
                "id": "",
                "biography": "",
                "url": ""
            }
        }
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(400, response.status_code)

    def test_user_valid_data(self):
        self.test_user_token()
        data = {
            "id": self.user.id,
            "first_name": "burak",
            "last_name": "güler",
            "profile": {
                "id": self.user.profile.id,
                "biography": "software eng",
                "url": "github"
            }
        }
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), data)
    """
