from django.urls import reverse
from rest_framework.test import APITestCase


class ReviewAPITestCase(APITestCase):
    viewname = "reviews"

    def test_api_exist(self):
        """
        test 'reviews' api is exist or not
        """

        reverse(viewname=self.viewname)
