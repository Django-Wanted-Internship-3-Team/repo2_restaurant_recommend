import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserDetailViewTest(APITestCase):
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

    def test_get_valid_user_success(self):
        response = self.client.get(
            path=reverse("user_detail"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_fail_unauthenticated(self):
        response = self.client.get(
            path=reverse("user_detail"),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_user_detail_update_success(self):
        response = self.client.patch(
            path=reverse("user_detail"),
            data=json.dumps({"latitude": "40.7132", "longitude": "-74.0060", "is_lunch_recommend": True}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_detail_update_fail(self):
        response = self.client.patch(
            path=reverse("user_detail"),
            data=json.dumps({"latitude": "40.7132", "longitude": "-74.0060", "is_lunch_recommend": True}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
