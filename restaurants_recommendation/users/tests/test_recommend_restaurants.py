from django.test import TestCase

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.users.models import User
from restaurants_recommendation.users.tasks import recommend_restaurants


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
