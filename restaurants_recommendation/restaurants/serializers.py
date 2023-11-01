from rest_framework import serializers

from restaurants_recommendation.restaurants.models import RestaurantLocation


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLocation
        fields = (
            "id",
            "do_si",
            "sgg",
            "longitude",
            "latitude",
        )
