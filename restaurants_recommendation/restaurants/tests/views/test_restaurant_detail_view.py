from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.reviews.models import Review
from restaurants_recommendation.users.models import User


class RestaurantListViewTest(APITestCase):
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
        pass
        # self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_get_restaurant_detail_success(self):
        response = self.client.get(
            path=self.view_url,
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # @TODO: 로그인 로직 구현 후 주석 풀기 @SaJH
    # def test_get_restaurant_detail_fail_unauthenticated(self):
    #     response = self.client.get(
    #       path=self.view_url,
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
