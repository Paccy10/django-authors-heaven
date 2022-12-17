from django.core.validators import RegexValidator
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from authors_heaven.settings.base import env

from ..common.utils import validate_unique_value
from .error_messages import errors
from .helpers.google import Google
from .helpers.utils import generate_username
from .models import AUTH_PROVIDERS, User

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


def generate_tokens(user):
    token = RefreshToken.for_user(user)

    return {
        "access_token": str(token.access_token),
        "refresh_token": str(token),
        "user": UserSerializer(user).data,
    }


def social_authenticate(**data):
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    name = data.get("name")
    provider = data.get("provider")

    user = User.objects.filter(email=email).first()

    if user:
        return generate_tokens(user)

    else:
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": generate_username(name),
            "email": email,
            "password": env("SOCIAL_SECRET"),
        }

        new_user = User.objects.create_user(**user_data)
        new_user.is_active = True
        new_user.auth_provider = provider
        new_user.save()

        return generate_tokens(new_user)


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
    password = password

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "auth_provider",
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

        if user.auth_provider != "email":
            raise AuthenticationFailed(
                errors["account"]["provider"].format(user.auth_provider)
            )

        elif not user.check_password(password):
            raise AuthenticationFailed(errors["account"]["no_account"])

        elif not user.is_active:
            raise AuthenticationFailed(errors["account"]["disabled"])

        else:
            return generate_tokens(user)


class ForgotPasswordSerializer(serializers.Serializer):
    """Forgot password serializer"""

    email = serializers.EmailField(
        error_messages={
            "required": errors["email"]["required"],
            "blank": errors["email"]["blank"],
            "invalid": errors["email"]["invalid"],
        },
    )


class ResetPasswordSerializer(serializers.Serializer):
    """Reset user password serializer"""

    password = password
    confirm_password = serializers.CharField(
        required=True,
        error_messages={
            "required": errors["confirm_password"]["required"],
            "blank": errors["confirm_password"]["blank"],
        },
    )

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError(
                {"passwords": errors["confirm_password"]["invalid"]}
            )

        return attrs


class GoogleAuthSerializer(serializers.Serializer):
    """Google authentication serializer"""

    auth_token = serializers.CharField(
        error_messages={
            "required": errors["auth_token"]["required"],
        },
    )

    def validate_auth_token(self, auth_token):
        try:
            user_data = Google.validate(auth_token)
        except ValueError as e:
            raise serializers.ValidationError(e)

        data = {
            "email": user_data.get("email"),
            "first_name": user_data.get("given_name"),
            "last_name": user_data.get("family_name"),
            "name": user_data.get("name"),
            "provider": AUTH_PROVIDERS.get("google"),
        }

        return social_authenticate(**data)
