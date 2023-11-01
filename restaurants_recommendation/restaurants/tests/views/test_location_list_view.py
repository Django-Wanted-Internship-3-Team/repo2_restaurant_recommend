import json

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
        pass
        # self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_get_location_list_success(self):
        response = self.client.get(
            path=self.view_url,
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # @TODO: 로그인 로직 구현 후 주석 풀기 @SaJH
    # def test_get_location_list_fail_unauthenticated(self):
    #     response = self.client.get(
    #         path=reverse("location_list"),
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
