from rest_framework import serializers

from restaurants_recommendation.restaurants.models import Restaurant, RestaurantLocation


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


class RestaurantDetailSerializer(serializers.ModelSerializer):
    location = LocationListSerializer()

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "restaurant_code",
            "location_code",
            "location",
            "business_name",
            "licensing_at",
            "operating_status",
            "closure_at",
            "floor_area",
            "water_supply_facility_type",
            "number_of_male_employees",
            "year",
            "multiple_use_facility",
            "grade_classification",
            "total_facility_size",
            "number_of_female_employees",
            "surrounding_area_description",
            "sanitary_business_type",
            "total_employees_count",
            "street_address",
            "parcel_address",
            "postal_code",
            "latitude",
            "longitude",
            "rating",
        )
