from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from ...common.serializers import BaseSerializer
from ...common.utils import validate_unique_value
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

    phone_number = serializers.SerializerMethodField()
    about_me = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

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

    def get_phone_number(self, user):
        return str(user.profile.phone_number) if user.profile.phone_number else None

    def get_about_me(self, user):
        return user.profile.about_me

    def get_avatar(self, user):
        request = self.context.get("request")
        avatar = user.profile.avatar
        return request.build_absolute_uri(avatar.url) if avatar else None

    def get_gender(self, user):
        return user.profile.gender

    def get_country(self, user):
        country = user.profile.country
        return country.name if country else None

    def get_city(self, user):
        return user.profile.city
