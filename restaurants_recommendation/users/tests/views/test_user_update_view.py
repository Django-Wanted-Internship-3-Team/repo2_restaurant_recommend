import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserUpdateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser1")
        cls.user.set_password("testpassword")
        cls.user.save()
        cls.user_data = {
            "username": "testuser1",
            "password": "testpassword",
        }

    def setUp(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(self.user_data),
            content_type="application/json",
        )
        self.access_token = response.data["token"]["access"]

    def test_valid_user_update(self):
        response = self.client.put(
            path=reverse("user_update", kwargs={"user_id": self.user.id}),
            data=json.dumps({"latitude": "40.7132", "longitude": "-74.0060", "is_lunch_recommend": True}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_update(self):
        response = self.client.put(
            path=reverse("user_update", kwargs={"user_id": self.user.id}),
            data=json.dumps({"latitude": "40.7132", "longitude": "-74.0060", "is_lunch_recommend": True}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
