from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authors_heaven.settings.base import env

from ..error_messages import errors
from ..helpers.facebook import Facebook
from ..helpers.google import Google
from ..helpers.twitter import Twitter
from ..helpers.utils import generate_username
from ..models import AUTH_PROVIDERS, User
from .user import generate_tokens


def social_authenticate(**data):
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    name = data.get("name")
    provider = data.get("provider")

    user = User.objects.filter(email=email).first()

    if user:
        if user.auth_provider != provider:
            user.auth_provider = provider
            user.save()

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


class GoogleAuthSerializer(serializers.Serializer):
    """Google authentication serializer"""

    auth_token = serializers.CharField(
        error_messages={
            "required": errors["auth_token"]["required"],
            "blank": errors["auth_token"]["blank"],
            "null": errors["auth_token"]["null"],
        },
    )

    def validate_auth_token(self, auth_token):
        try:
            user_data = Google.validate(auth_token)
        except ValueError as e:
            raise serializers.ValidationError(e)

        if user_data["aud"] != env("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed(errors["social_app_id"]["invalid"])

        data = {
            "email": user_data.get("email"),
            "first_name": user_data.get("given_name"),
            "last_name": user_data.get("family_name"),
            "name": user_data.get("name"),
            "provider": AUTH_PROVIDERS.get("google"),
        }

        return social_authenticate(**data)


class FacebookAuthSerializer(serializers.Serializer):
    """Facebook authentication serializer"""

    auth_token = serializers.CharField(
        error_messages={
            "required": errors["auth_token"]["required"],
            "blank": errors["auth_token"]["blank"],
            "null": errors["auth_token"]["null"],
        },
    )

    def validate_auth_token(self, auth_token):
        try:
            profile = Facebook.validate(auth_token)
        except ValueError as e:
            raise serializers.ValidationError(e)

        data = {
            "email": profile.get("email"),
            "first_name": profile.get("first_name"),
            "last_name": profile.get("last_name"),
            "name": profile.get("name"),
            "provider": AUTH_PROVIDERS.get("facebook"),
        }

        return social_authenticate(**data)


class TwitterAuthSerializer(serializers.Serializer):
    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()

    def validate(self, attrs):
        access_token_key = attrs.get("access_token_key")
        access_token_secret = attrs.get("access_token_secret")

        try:
            profile = Twitter.validate(access_token_key, access_token_secret)
        except ValueError as e:
            raise serializers.ValidationError({"access_tokens": e})

        name = profile.get("name")
        names = name.split(" ")
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else names[0]

        data = {
            "email": profile.get("email"),
            "first_name": first_name,
            "last_name": last_name,
            "name": name,
            "provider": AUTH_PROVIDERS.get("twitter"),
        }

        return social_authenticate(**data)
