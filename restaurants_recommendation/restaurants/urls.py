from typing import List

from django.urls import URLPattern, path

from restaurants_recommendation.restaurants.views import (
    LocationListView,
    RestaurantDetailView,
    RestaurantListView,
)

urlpatterns: List[URLPattern] = [
    path("locations/", LocationListView.as_view(), name="location_list"),
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:restaurant_id>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
]
