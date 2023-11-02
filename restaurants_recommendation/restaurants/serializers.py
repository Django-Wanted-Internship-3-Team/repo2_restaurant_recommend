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


class RestaurantQuerySerializer(serializers.Serializer):
    lat = serializers.CharField(required=True)
    lon = serializers.CharField(required=True)
    range = serializers.FloatField(default=1.0)
    order_by = serializers.CharField(required=False, default="distance")
    type = serializers.CharField(required=False, default="my_location")
    search = serializers.CharField(required=False, default="")
    limit = serializers.IntegerField(required=False, default=10, max_value=30)
    offset = serializers.IntegerField(required=False, default=0)


class RestaurantListSerializer(serializers.ModelSerializer):
    location = LocationListSerializer()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "restaurant_code",
            "location_code",
            "location",
            "business_name",
            "operating_status",
            "closure_at",
            "street_address",
            "parcel_address",
            "postal_code",
            "latitude",
            "longitude",
            "rating",
            "distance",
        )

    def get_distance(self, obj):
        return f"{obj.distance} km"
      
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
