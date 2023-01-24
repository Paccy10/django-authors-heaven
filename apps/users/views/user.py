from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...common.utils import should_be_admin
from ...profiles.models import Profile
from ...profiles.serializers import (
    EditProfileSerializer,
    ProfileDisplaySerializer,
    UserProfileSerializer,
)
from ..models import User
from ..serializers import UserDisplaySerializer


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


class UsersView(mixins.ListModelMixin, generics.GenericAPIView):
    """Get all users view"""

    queryset = User.objects.all()
    serializer_class = UserDisplaySerializer
    permission_classes = [IsAuthenticated]
    ordering = ["-pkid"]
    search_fields = [
        "first_name",
        "last_name",
        "middle_name",
        "username",
        "email",
        "profile__phone_number",
        "profile__country",
        "profile__city",
    ]

    @should_be_admin()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Get single user view"""

    queryset = User.objects.all()
    serializer_class = UserDisplaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    @should_be_admin()
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserProfileView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Get another user profile view"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
