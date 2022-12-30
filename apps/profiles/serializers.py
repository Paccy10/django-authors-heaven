from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .models import Gender, Profile


class ProfileDisplaySerializer(serializers.ModelSerializer):
    """User profile display serializer"""

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
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

    def get_first_name(self, profile):
        return profile.user.first_name

    def get_last_name(self, profile):
        return profile.user.last_name

    def get_middle_name(self, profile):
        return profile.user.middle_name

    def get_email(self, profile):
        return profile.user.email

    def get_username(self, profile):
        return profile.user.username

    def get_country(self, profile):
        return profile.country.name


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
