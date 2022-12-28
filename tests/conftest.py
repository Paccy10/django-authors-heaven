import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories.profile import ProfileFactory
from .factories.user import ActiveUserFactory, UserFactory

register(UserFactory)
register(ProfileFactory)
register(ActiveUserFactory)


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def active_user(db, user_factory):
    new_user = user_factory.create()
    new_user.is_active = True
    new_user.save()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True)
    return new_user


@pytest.fixture
def profile(db, profile_factory):
    user_profile = profile_factory.create()
    return user_profile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_api_client(db, active_user_factory):
    new_user = active_user_factory.create()
    new_user.is_active = True
    new_user.save()

    token = RefreshToken.for_user(new_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")

    return client
