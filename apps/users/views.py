import django_rq
import jwt
from django.template.loader import get_template
from django.urls import reverse
from rest_framework import generics, mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authors_heaven.settings.base import env

from ..common.utils import send_email
from ..profiles.models import Profile
from ..profiles.serializers import EditProfileSerializer, ProfileDisplaySerializer
from .error_messages import errors
from .models import User
from .serializers import (
    FacebookAuthSerializer,
    ForgotPasswordSerializer,
    GoogleAuthSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    TwitterAuthSerializer,
    UserSerializer,
)


class UserSignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    """User signup view"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)

        # Send verification email
        user = User.objects.get(id=response.data["id"])
        token = RefreshToken.for_user(user).access_token
        current_path = reverse("verify")
        url = "http://" + request.get_host() + current_path + "?token=" + str(token)
        subject = "Email Verification"
        message = get_template("verification.html").render({"user": user, "url": url})
        django_rq.enqueue(send_email, subject, message, [user.email])

        return response


class UserVerificationView(generics.GenericAPIView):
    """User verification view"""

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, env("SECRET_KEY"), algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])

            if not user.is_active:
                user.is_active = True
                user.save()

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(
                {"token": [errors["token"]["expired"]]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.DecodeError:
            return Response(
                {"token": [errors["token"]["invalid"]]},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView(generics.GenericAPIView):
    """User login view"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ForgotPasswordView(generics.GenericAPIView):
    """Forgot password view"""

    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if not user:
            raise NotFound(f"User with email '{email}' not found")

        token = RefreshToken.for_user(user).access_token
        current_path = reverse("reset-password")
        url = "http://" + request.get_host() + current_path + "?token=" + str(token)
        subject = "Forgot Password"
        message = get_template("forgot-password.html").render(
            {"user": user, "url": url}
        )
        django_rq.enqueue(send_email, subject, message, [user.email])

        return Response(
            {
                "detail": "Password reset link successfully sent. Please check your email to continue"
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(generics.GenericAPIView):
    """Reset password view"""

    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, env("SECRET_KEY"), algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])

            user.set_password(serializer.validated_data["password"])
            user.save()

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(
                {"token": [errors["token"]["expired"]]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.DecodeError:
            return Response(
                {"token": [errors["token"]["invalid"]]},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GoogleAuthView(generics.GenericAPIView):
    """Google authentication view"""

    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data["auth_token"]

        return Response(data, status=status.HTTP_200_OK)


class FacebookAuthView(generics.GenericAPIView):
    """Facebook authentication view"""

    serializer_class = FacebookAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data["auth_token"]

        return Response(data, status=status.HTTP_200_OK)


class TwitterAuthView(generics.GenericAPIView):
    """Twitter authentication view"""

    serializer_class = TwitterAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        return Response(data, status=status.HTTP_200_OK)


class MyProfileView(generics.GenericAPIView):
    """User own profile view"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        data = ProfileDisplaySerializer(profile, context={"request": request}).data

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = EditProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user_data = {k: data.get(k) for k in ["first_name", "last_name", "middle_name"]}
        profile_data = {
            k: data.get(k)
            for k in ["phone_number", "about_me", "avatar", "gender", "country", "city"]
        }
        profile = Profile.objects.get(user=request.user)

        for attr, value in user_data.items():
            setattr(profile.user, attr, value)
        profile.user.save()

        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return Response(
            ProfileDisplaySerializer(profile, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )
