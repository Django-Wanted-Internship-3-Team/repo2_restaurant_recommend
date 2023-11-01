from typing import Callable, List

from django.urls import path

from restaurants_recommendation.reviews.views import ReviewAPIView

urlpatterns: List[Callable] = [
    path(r"", ReviewAPIView.as_view(), name="reviews"),
]
