from django.core.validators import RegexValidator
from django.db.models import Q
from rest_framework import serializers

from ..common.utils import validate_unique_value
from .error_messages import errors
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    first_name = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["first_name"]["required"],
            "blank": errors["first_name"]["blank"],
        },
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["last_name"]["required"],
            "blank": errors["last_name"]["blank"],
        },
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": errors["email"]["required"],
            "blank": errors["email"]["blank"],
            "invalid": errors["email"]["invalid"],
        },
    )
    username = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["username"]["required"],
            "blank": errors["username"]["blank"],
        },
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=100,
        write_only=True,
        validators=[
            RegexValidator(
                regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).+$",
                message=errors["password"]["weak"],
            )
        ],
        error_messages={
            "required": errors["password"]["required"],
            "blank": errors["password"]["blank"],
            "min_length": errors["password"]["min_length"],
        },
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_active",
            "created_at",
        ]

    def validate_email(self, email):
        norm_email = email.lower()
        validate_unique_value(
            model=User,
            field="email",
            value=norm_email,
            errors=errors,
            instance=self.instance,
        )

        return norm_email

    def validate_username(self, username):
        validate_unique_value(
            model=User,
            field="username",
            value=username,
            errors=errors,
            instance=self.instance,
        )

        return username

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """User login serializer"""

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        write_only=True,
        error_messages={
            "required": errors["password"]["required"],
        },
    )

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")

        if not email and not username:
            raise serializers.ValidationError(
                {"username": errors["account"]["required"]}
            )

        try:
            user = User.objects.get(Q(username=username) | Q(email=email))
        except User.DoesNotExist:
            raise AuthenticationFailed(errors["account"]["no_account"])

        if not user.check_password(password):
            raise AuthenticationFailed(errors["account"]["no_account"])

        if not user.is_active:
            raise AuthenticationFailed(errors["account"]["disabled"])

        token = RefreshToken.for_user(user)

        return {
            "access_token": str(token.access_token),
            "refresh_token": str(token),
            "user": UserSerializer(user).data,
        }
