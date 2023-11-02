from typing import List

from django.urls import URLPattern, path

from restaurants_recommendation.reviews.views import ReviewAPIView

urlpatterns: List[URLPattern] = [
    path(r"", ReviewAPIView.as_view(), name="reviews"),
]
