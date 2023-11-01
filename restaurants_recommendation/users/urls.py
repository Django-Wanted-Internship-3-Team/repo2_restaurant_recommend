from typing import Callable, List

from django.urls import URLPattern, path

from restaurants_recommendation.users.views import SignupView

urlpatterns: List[URLPattern] = [
    path("signup/", SignupView.as_view(), name="signup"),
]
