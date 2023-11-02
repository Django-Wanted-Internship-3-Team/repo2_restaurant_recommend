import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.users.models import User


class ReviewAPITestCase(APITestCase):
    viewname = "reviews"

    def test_post_api_exist(self):
        """
        test 'reviews' api is exist or not
        """

        reverse(viewname=self.viewname)

    def test_post_without_auth(self):
        """
        test 'reviews' post api, without auth
        expected 401
        """

        user = User.objects.create(username="user")
        restaurant = Restaurant.objects.create(restaurant_code="abc")

        response = self.client.post(
            reverse(self.viewname),
            data=json.dumps(
                {
                    "content": "content",
                    "rating": 1,
                    "restaurant": restaurant.id,
                    "user": user.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED, msg="expected 401")

    def test_post_with_auth(self):
        """
        test 'reviews' post api, with auth,
        expected 201 and create review
        """
        user = User.objects.create(username="user")
        restaurant = Restaurant.objects.create(restaurant_code="abc", business_name="name")

        self.client.force_authenticate(user)

        response = self.client.post(
            reverse(self.viewname),
            data=json.dumps(
                {
                    "content": "content",
                    "rating": 1,
                    "restaurant": restaurant.id,
                    "user": user.id,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="expected 201")

    def test_post_with_auth_invalid_rating_under0(self):
        """
        test 'reviews' post api and invalid rating
        expected 400
        """

        user = User.objects.create(username="user")
        restaurant = Restaurant.objects.create(restaurant_code="abc")

        self.client.force_authenticate(user)

        response = self.client.post(
            reverse(self.viewname),
            data=json.dumps(
                {
                    "content": "content",
                    "rating": -1,
                    "restaurant": restaurant.id,
                    "user": user.id,
                },
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_auth_invalid_rating_over5(self):
        """
        test 'reviews' post api and invalid rating
        expected 400
        """

        user = User.objects.create(username="user")
        restaurant = Restaurant.objects.create(restaurant_code="abc")

        self.client.force_authenticate(user)

        response = self.client.post(
            reverse(self.viewname),
            data=json.dumps(
                {
                    "content": "content",
                    "rating": 6,
                    "restaurant": restaurant.id,
                    "user": user.id,
                },
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_auth_invalid_restaurant(self):
        """
        test
        """

        user = User.objects.create(username="user")
        self.client.force_authenticate(user)

        response = self.client.post(
            reverse(self.viewname),
            data=json.dumps(
                {
                    "content": "content",
                    "rating": 5,
                    "restaurant": 2,
                    "user": user.id,
                },
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
