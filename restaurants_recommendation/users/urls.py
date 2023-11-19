from typing import List

from django.urls import URLPattern, path
from rest_framework_simplejwt.views import TokenRefreshView

from restaurants_recommendation.users.views import LoginView, SignupView, UserDetailView

urlpatterns: List[URLPattern] = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", UserDetailView.as_view(), name="user_detail"),
]
