from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants_recommendation.restaurants.models import Restaurant, RestaurantLocation
from restaurants_recommendation.users.models import User


class RestaurantListViewTest(APITestCase):
    view_url = reverse("restaurant_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test", password="test")
        cls.user_data = {
            "username": "test",
            "password": "test",
        }
        cls.restaurant_location = RestaurantLocation.objects.create(
            do_si="서울특별시",
            sgg="강남구",
            latitude="37.514575",
            longitude="127.0495556",
        )

        cls.restaurant_1 = Restaurant.objects.create(
            restaurant_code="서울역",
            business_name="서울역",
            location=cls.restaurant_location,
            rating=3.0,
            latitude="37.552411117508086",
            longitude="126.97097221142944",
        )
        cls.restaurant_2 = Restaurant.objects.create(
            restaurant_code="용산역",
            business_name="용산역",
            location=cls.restaurant_location,
            rating=4.0,
            latitude="37.52894651237838",
            longitude="126.9619306425219",
        )

    def setUp(self):
        pass
        # self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    def test_get_restaurant_list_type_hold_location_success(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "hold_location",
                "lat": "37.514575",
                "lon": "127.0495556",
                "range": 100.0,
                "order_by": "distance",
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["results"][0]["restaurant_code"], "서울역")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_list_type_my_location_success(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "my_location",
                "lat": "37.56628801692559",
                "lon": "126.97814305793757",
                "range": 100.0,
                "order_by": "distance",
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["results"][0]["restaurant_code"], "서울역")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_list_order_by_distance_success(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "hold_location",
                "lat": "37.514575",
                "lon": "127.0495556",
                "range": 100.0,
                "order_by": "distance",
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["results"][0]["restaurant_code"], "서울역")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_list_order_by_rating_success(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "hold_location",
                "lat": "37.514575",
                "lon": "127.0495556",
                "range": 100.0,
                "order_by": "rating",
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["results"][0]["restaurant_code"], "용산역")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_list_search_success(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "hold_location",
                "lat": "37.514575",
                "lon": "127.0495556",
                "range": 100.0,
                "order_by": "distance",
                "search": "용산역",
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["results"][0]["restaurant_code"], "용산역")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_list_pagination_success(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "hold_location",
                "lat": "37.514575",
                "lon": "127.0495556",
                "range": 100.0,
                "order_by": "distance",
                "limit": 1,
                "offset": 1,
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["results"][0]["restaurant_code"], "용산역")
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["total_count"], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_list_fail_invalid_filter_type(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "invalid",
                "lat": "37.514575",
                "lon": "127.0495556",
                "range": 100.0,
                "order_by": "distance",
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_restaurant_list_fail_not_enough_params(self):
        response = self.client.get(
            path=self.view_url,
            data={
                "type": "hold_location",
                "range": 100.0,
            }
            # HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # @TODO: 로그인 로직 구현 후 주석 풀기 @SaJH
    # def test_get_restaurant_list_fail_unauthenticated(self):
    # response = self.client.get(
    #     path=self.view_url,
    #     data={
    #         "type": "hold_location",
    #         "lat": "37.514575",
    #         "lon": "127.0495556",
    #         "range": 100.0,
    #         "order_by": "distance",
    #         "search": "용산역",
    #     }
    # )
    # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
