import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from comment.models import Comment
from restaurant.models import Restaurant

login_url = reverse("token_obtain_pair")


class CommentCreateTestCase(APITestCase):
    def setUp(self):
        self.create_url = reverse("comment:create")
        self.list_url = reverse("comment:list")
        self.data = {
            "username": "burak_comm",
            "password": "burak123"
        }
        self.restaurant = Restaurant.objects.create(name="Comment", location="a", cuisine="b", slug="comm-test")
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])
        self.parent_comment = Comment.objects.create(content="content1", user=self.user, restaurant=self.restaurant)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(login_url, data=self.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_comment(self):
        data = {
            "content": "first comment",
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "parent": ""
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(201, response.status_code)

    def test_create_child_comment(self):
        data = {
            "content": "child comment 1",
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "parent": self.parent_comment.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(201, response.status_code)

    def test_comment_list(self):
        self.test_create_comment()
        response = self.client.get(self.list_url, {'res': self.restaurant.id})
        self.assertTrue(response.data["count"] == Comment.objects.filter(restaurant=self.restaurant).count())


class CommentUpdateDeleteTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "burak_comment",
            "password": "burak123"
        }
        self.restaurant = Restaurant.objects.create(name="Comment", location="a", cuisine="b", slug="comm-test")
        self.user = User.objects.create_user(username=self.data["username"], password=self.data["password"])
        self.other_user = User.objects.create_user(username="other_burak", password=self.data["password"])
        self.comment = Comment.objects.create(content="other_comment", user=self.user, restaurant=self.restaurant)
        self.update_url = reverse("comment:update", kwargs={'pk': self.comment.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="burak_comment", password="burak123"):
        response = self.client.post(login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_delete_comment(self):
        response = self.client.delete(self.update_url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_another_user(self):
        self.test_jwt_authentication("other_burak")
        response = self.client.delete(self.update_url)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.objects.get(pk=self.comment.pk))

    def test_update_comment(self):
        response = self.client.put(self.update_url, data={"content": "updated comment"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Comment.objects.get(pk=self.comment.id).content, "updated comment")

    def test_update_comment_another_user(self):
        self.test_jwt_authentication("other_burak")
        response = self.client.put(self.update_url, data={"content": "update!!"})
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Comment.objects.get(pk=self.comment.id).content, "update!!")

    def test_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.update_url)
        self.assertEqual(401, response.status_code)
