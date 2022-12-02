import pytest
from pytest_factoryboy import register

from .factories.profile import ProfileFactory
from .factories.user import UserFactory

register(UserFactory)
register(ProfileFactory)


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True)
    return new_user


@pytest.fixture
def profile(db, profile_factory):
    user_profile = profile_factory.create()
    return user_profile
