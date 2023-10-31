from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
