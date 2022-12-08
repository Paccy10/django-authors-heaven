from rest_framework import generics, mixins

from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import django_rq
from django.template.loader import get_template
from ..common.utils import send_email
from django.urls import reverse
import jwt
from authors_heaven.settings.base import env
from rest_framework import status
from rest_framework.response import Response
from .error_messages import errors


class UserSignupView(mixins.CreateModelMixin, generics.GenericAPIView):
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
