from django.urls import path

from restaurants_recommendation.restaurants.views import LocationListView

urlpatterns = [
    path("locations/", LocationListView.as_view(), name="location_list"),
]
