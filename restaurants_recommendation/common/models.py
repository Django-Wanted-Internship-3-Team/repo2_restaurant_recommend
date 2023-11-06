import math

from django.db import models

from restaurants_recommendation.common.utils import lat_lon_to_km


class LatLonModelBase(models.Model):
    latitude = models.CharField(max_length=32, null=True)
    longitude = models.CharField(max_length=32, null=True)

    class Meta:
        abstract = True

    def distance_with(self, o):
        try:
            position = [float(self.latitude), float(self.longitute)]
            postition_o = [float(o.latitude), float(o.longitude)]
        except:
            return math.inf

        return lat_lon_to_km(position, postition_o)
