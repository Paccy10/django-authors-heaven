from rest_framework import serializers

from .models import Profile


class ProfileDisplaySerializer(serializers.ModelSerializer):
    """User profile display serializer"""

    first_name = serializers.SerializerMethodField(method_name="get_first_name")
    last_name = serializers.SerializerMethodField(method_name="get_last_name")
    middle_name = serializers.SerializerMethodField(method_name="get_middle_name")
    email = serializers.SerializerMethodField(method_name="get_email")
    username = serializers.SerializerMethodField(method_name="get_username")
    country = serializers.SerializerMethodField(method_name="get_country")

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
