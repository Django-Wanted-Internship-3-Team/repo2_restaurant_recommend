import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password="testpassword")

    def test_post_signup_success(self):
        response = self.client.post(
            path=reverse("signup"),
            data=json.dumps({"username": "testuser2", "password": "testpassword"}),
            content_type="application/json",
        )
        response_data = json.loads(response.content)
        self.assertEqual(response_data["username"], "testuser2")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_signup_fail_invalid_password(self):
        response = self.client.post(
            path=reverse("signup"),
            data={"username": "testuser3", "password": "1010"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_similarity_validator(self):
        response = self.client.post(
            path=reverse("signup"),
            data={"username": "testuser3", "password": "testuser312"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
