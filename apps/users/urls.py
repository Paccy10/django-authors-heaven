from django.urls import path

from .views import (
    FacebookAuthView,
    ForgotPasswordView,
    GoogleAuthView,
    MyProfileView,
    ResetPasswordView,
    TwitterAuthView,
    UserLoginView,
    UserSignupView,
    UsersView,
    UserVerificationView,
    UserView,
)

urlpatterns = [
    path("auth/signup/", UserSignupView.as_view(), name="signup"),
    path("auth/verify/", UserVerificationView.as_view(), name="verify"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/facebook/", FacebookAuthView.as_view(), name="facebook-auth"),
    path("auth/twitter/", TwitterAuthView.as_view(), name="twitter-auth"),
    path("profile/me/", MyProfileView.as_view(), name="my-profile"),
    path("", UsersView.as_view(), name=("get-users")),
    path("<slug:id>/", UserView.as_view(), name=("get-user")),
]
