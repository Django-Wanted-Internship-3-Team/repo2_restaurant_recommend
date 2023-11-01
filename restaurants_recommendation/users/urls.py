from django.urls import path
from typing import Callable, List

from users.views import SignupView

urlpatterns: List[Callable] = [
    path("signup/", SignupView.as_view(), name="signup"),
]
