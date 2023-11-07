from datetime import datetime
from unittest import mock

from django.test import TestCase
from rest_framework import status

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.users.models import User
from restaurants_recommendation.users.tasks import (
    post_webhook,
    recommend_restaurants,
    recommend_restaurants_to_user,
)


def discord_webhook_mock(url, json):
    mock_response = mock.Mock()
    mock_response.status_code = 200

    return mock_response


class RecommendRestaurantsTestCase(TestCase):
    def test_recommend_restaurants(self):
        user = User.objects.create(
            username="user",
            latitude="40.7132",
            longitude="-70.0060",
        )

        restaurant_in_0 = Restaurant.objects.create(
            restaurant_code="in0",
            latitude="40.7132",
            longitude="-70.0060",
            rating=0,
        )

        restaurant_notin_0 = Restaurant.objects.create(
            restaurant_code="notin0",
            latitude="40.8132",
            longitude="-70.0060",
            rating=5,
        )

        restaurants = recommend_restaurants(user)

        self.assertIn(restaurant_in_0, restaurants)
        self.assertNotIn(restaurant_notin_0, restaurants)

    @mock.patch("requests.post", side_effect=discord_webhook_mock)
    def test_webhook(self, mock_post):
        user = User.objects.create(
            username="user",
            latitude="40.7000",
            longitude="-70.0060",
            is_lunch_recommend=True,
            webhook="test-webhook-url",
        )

        response = post_webhook(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch("requests.post", side_effect=discord_webhook_mock)
    @mock.patch("django.utils.timezone.now")
    def test_recommend_restaurant_scheduler(self, mock_now, mock_request):
        # TODO : 주말, 주간 나눠서 테스트 필요.
        mock_now.return_value = datetime(2023, 11, 6, 12, 0, 0)  # mon

        User.objects.create(
            username="user",
            latitude="40.7132",
            longitude="-70.0060",
            is_lunch_recommend=True,
            webhook=f"test_webhook-url",
        )

        Restaurant.objects.create(
            restaurant_code="1",
            business_name="서브웨이",
            latitude="40.7132",
            longitude="-70.0060",
            rating=0,
        )

        Restaurant.objects.create(
            restaurant_code="2",
            business_name="짬뽕나라",
            latitude="40.8132",
            longitude="-70.0060",
            rating=5,
        )
        Restaurant.objects.create(
            restaurant_code="3",
            business_name="맥도날드",
            latitude="40.71325",
            longitude="-70.0060",
            rating=5,
        )
        Restaurant.objects.create(
            restaurant_code="4",
            business_name="만리장성",
            latitude="40.71324",
            longitude="-70.0060",
            rating=5,
        )
        Restaurant.objects.create(
            restaurant_code="5",
            business_name="다온",
            latitude="40.71326",
            longitude="-70.0060",
            rating=5,
        )

        result = recommend_restaurants_to_user.apply()
        self.assertTrue(result.successful())
