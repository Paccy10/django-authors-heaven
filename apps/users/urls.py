from django.urls import path

from .views import UserLoginView, UserSignupView, UserVerificationView

urlpatterns = [
    path("auth/signup/", UserSignupView.as_view(), name="signup"),
    path("auth/verify/", UserVerificationView.as_view(), name="verify"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
]
