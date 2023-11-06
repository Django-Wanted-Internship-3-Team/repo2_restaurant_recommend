from datetime import datetime
from unittest import mock

from django.test import TestCase

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.users.models import User
from restaurants_recommendation.users.tasks import (
    recommend_restaurants,
    recommend_restaurants_to_user,
)


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

    @mock.patch("django.utils.timezone.now")
    def test_recommend_restaurant_scheduler(self, mock_now):
        mock_now.return_value = datetime(2023, 11, 6, 12, 0, 0)  # mon

        result = recommend_restaurants_to_user.apply()
        self.assertTrue(result.successful())

    @mock.patch("django.utils.timezone.now")
    def test_recommend_restaurant_scheduler_on_weekend(self, mock_now):
        """스케줄 주기 평일 12시가 아닌 주말 시간에 task가 수행되는지 테스트"""
        # TODO :
        mock_now.return_value = datetime(2023, 11, 5, 12, 0, 0)

        result = recommend_restaurants_to_user.apply()

        self.assertFalse(result.successful())
