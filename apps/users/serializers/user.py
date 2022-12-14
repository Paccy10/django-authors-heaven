from django.core.validators import RegexValidator
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from ...common.serializers import BaseSerializer
from ...common.utils import get_country_name, validate_unique_value
from ..error_messages import errors
from ..models import User

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
            "first_name",
            "last_name",
            "username",
            "email",
            "auth_provider",
            "password",
            "is_active",
        ] + BaseSerializer.Meta.fields

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


class UserDisplaySerializer(serializers.ModelSerializer):
    """User display serializer"""

    phone_number = PhoneNumberField(source="profile.phone_number")
    about_me = serializers.CharField(source="profile.about_me")
    avatar = serializers.ImageField(source="profile.avatar")
    gender = serializers.CharField(source="profile.gender")
    country = serializers.SerializerMethodField()
    city = serializers.CharField(source="profile.city")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "auth_provider",
            "is_active",
            "is_admin",
            "phone_number",
            "about_me",
            "avatar",
            "gender",
            "country",
            "city",
        ] + BaseSerializer.Meta.fields

    def get_country(self, user):
        return get_country_name(user.profile.country)
