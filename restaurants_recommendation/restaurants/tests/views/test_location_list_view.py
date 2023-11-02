import json

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants_recommendation.restaurants.models import RestaurantLocation
from restaurants_recommendation.users.models import User


class LocationListViewTest(APITestCase):
    fixtures = ["data/location.json"]
    view_url = reverse("location_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test", password="test")
        cls.user_data = {
            "username": "test",
            "password": "test",
        }
        with open("data/location.json", "r") as f:
            cls.location_data = json.load(f)

            RestaurantLocation.objects.bulk_create(
                RestaurantLocation(
                    do_si=location["fields"]["do_si"],
                    sgg=location["fields"]["sgg"],
                    latitude=location["fields"]["latitude"],
                    longitude=location["fields"]["longitude"],
                )
                for location in cls.location_data
            )

    def setUp(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(self.user_data),
            content_type="application/json",
        )
        self.access_token = response.data["token"]["access"]

    def test_get_location_list_success(self):
        response = self.client.get(
            path=self.view_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_location_list_cache_success(self):
        response = self.client.get(
            path=self.view_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get("locations"))
        cache.clear()

    def test_get_location_list_fail_unauthenticated(self):
        response = self.client.get(
            path=self.view_url,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
