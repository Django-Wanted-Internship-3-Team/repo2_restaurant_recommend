from django.urls import path

from restaurant_recommendation.users.views import SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
