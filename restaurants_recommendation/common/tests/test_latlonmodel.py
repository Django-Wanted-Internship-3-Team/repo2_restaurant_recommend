from django.test import TestCase

from restaurants_recommendation.common.models import LatLonModelBase


class LatLonModelBaseTestCase(TestCase):
    class TestLatLonModel(LatLonModelBase):
        pass

    def test_distance_with(self):
        obj1 = self.TestLatLonModel.objects.create(latitude="70.000", longitude="-70.000")
        obj2 = self.TestLatLonModel.objects.create(latitude="70.001", longitude="=70.001")

        distance = obj1.distance_with(obj2)
        self.assertEqual(type(distance), float)
