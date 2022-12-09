from django.urls import path

from .views import UserSignupView, UserVerificationView

urlpatterns = [
    path("auth/signup/", UserSignupView.as_view(), name="signup"),
    path("auth/verify/", UserVerificationView.as_view(), name="verify"),
]
