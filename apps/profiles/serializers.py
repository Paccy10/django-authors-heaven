from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from ..common.utils import get_country_name
from ..users.models import User
from .models import Gender, Profile


class ProfileDisplaySerializer(serializers.ModelSerializer):
    """User profile display serializer"""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    middle_name = serializers.CharField(source="user.middle_name")
    email = serializers.CharField(source="user.email")
    username = serializers.CharField(source="user.username")
    country = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "username",
            "phone_number",
            "about_me",
            "avatar",
            "gender",
            "country",
            "city",
            "created_at",
        ]

    def get_country(self, profile):
        return get_country_name(profile.country)


class EditProfileSerializer(serializers.Serializer):
    """Edit user profile serializer"""

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    phone_number = PhoneNumberField()
    about_me = serializers.CharField()
    avatar = serializers.ImageField(required=False)
    gender = serializers.ChoiceField(choices=Gender.choices)
    country = CountryField(name_only=True)
    city = serializers.CharField()

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "phone_number",
            "about_me",
            "avatar",
            "gender",
            "country",
            "city",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """Another user profile serializer"""

    about_me = serializers.CharField(source="profile.about_me")
    gender = serializers.CharField(source="profile.gender")
    city = serializers.CharField(source="profile.city")
    avatar = serializers.ImageField(source="profile.avatar")
    country = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "about_me",
            "avatar",
            "gender",
            "country",
            "city",
        ]

    def get_country(self, user):
        return get_country_name(user.profile.country)
