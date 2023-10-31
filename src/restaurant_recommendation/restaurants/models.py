from django.db import models


class Restaurant(models.Model):
    restaurant_code = models.CharField(max_length=128, unique=True)
    location = models.CharField(max_length=128, null=True)
    location_code = models.CharField(max_length=64, null=True)
    business_name = models.CharField(max_length=64, null=True)
    licensing_at = models.CharField(max_length=16, null=True)
    operating_status = models.CharField(max_length=16, null=True)
    closure_at = models.CharField(max_length=16, null=True)
    floor_area = models.CharField(max_length=32, null=True)
    water_supply_facility_type = models.CharField(max_length=32, null=True)
    number_of_male_employees = models.IntegerField(null=True)
    year = models.CharField(max_length=32, null=True)
    multiple_use_facility = models.CharField(max_length=32, null=True)
    grade_classification = models.CharField(max_length=32, null=True)
    total_facility_size = models.CharField(max_length=32, null=True)
    number_of_female_employees = models.IntegerField(null=True)
    surrounding_area_description = models.CharField(max_length=32, null=True)
    sanitary_business_type = models.CharField(max_length=32, null=True)
    total_employees_count = models.IntegerField(null=True)
    street_address = models.CharField(max_length=32, null=True)
    parcel_address = models.CharField(max_length=32, null=True)
    postal_code = models.CharField(max_length=32, null=True)
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    rating = models.FloatField(null=True)

    class Meta:
        db_table = "restaurants"

    def __str__(self):
        return self.business_name
