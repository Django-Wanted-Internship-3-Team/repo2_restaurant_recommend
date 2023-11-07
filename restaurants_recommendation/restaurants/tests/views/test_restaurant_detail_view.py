import json

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.reviews.models import Review
from restaurants_recommendation.users.models import User


class RestaurantDetailViewTest(APITestCase):
    view_url = reverse("restaurant_detail", kwargs={"restaurant_id": 1})

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test", password="test")
        cls.user_data = {
            "username": "test",
            "password": "test",
        }
        cls.restaurant = Restaurant.objects.create(
            restaurant_code="test",
            latitude="test",
            longitude="test",
        )
        for i in range(10):
            cls.review = Review.objects.create(
                user=cls.user,
                restaurant=cls.restaurant,
                rating=5,
                content=f"test{i}",
            )

    def setUp(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(self.user_data),
            content_type="application/json",
        )
        self.access_token = response.data["token"]["access"]

    def test_get_restaurant_detail_success(self):
        response = self.client.get(
            path=self.view_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_detail_cache_success(self):
        response = self.client.get(
            path=self.view_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get("restaurant_detail:1"))
        cache.clear()

    def test_get_restaurant_detail_fail_unauthenticated(self):
        response = self.client.get(
            path=self.view_url,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
