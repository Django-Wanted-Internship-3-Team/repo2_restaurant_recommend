import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser1")
        self.user.set_password("testpassword")
        self.user.save()

    def test_user_login_success(self):
        response = self.client.post(
            path=reverse("login"), data=json.dumps({"username": "testuser1", "password": "testpassword"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_not_found(self):
        response = self.client.post(
            path=reverse("login"), data=json.dumps({"username": "testuser2", "password": "testpassword"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_failure_invalid_password(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps({"username": "testuser1", "password": "invalid_password"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
