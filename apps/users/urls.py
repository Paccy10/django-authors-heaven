from django.urls import path

from .views import UserSignupView

urlpatterns = [
    path("auth/signup/", UserSignupView.as_view(), name="signup"),
]
