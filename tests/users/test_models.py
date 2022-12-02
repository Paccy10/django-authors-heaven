import pytest

from apps.users.error_messages import errors


class TestUserModel:
    """Test user model"""

    def test_user_str(self, base_user):
        assert base_user.__str__() == f"{base_user.username}"

    def test_get_full_name(self, base_user):
        fullname = f"{base_user.first_name.title()} {base_user.last_name.title()}"

        assert base_user.get_full_name == fullname

    def test_user_email_is_normalized(self, base_user):
        email = "TEST@example.COM"

        assert base_user.email == email.lower()

    def test_base_user_is_not_activated(self, base_user):
        assert base_user.is_active is False

    def test_super_user_is_activated(self, super_user):
        assert super_user.is_active is True

    def test_create_user_without_username_fails(self, user_factory):
        with pytest.raises(ValueError) as error:
            user_factory.create(username=None)

        assert str(error.value) == errors["username"]["required"]

    def test_create_user_without_first_name_fails(self, user_factory):
        with pytest.raises(ValueError) as error:
            user_factory.create(first_name=None)

        assert str(error.value) == errors["first_name"]["required"]

    def test_create_user_without_last_name_fails(self, user_factory):
        with pytest.raises(ValueError) as error:
            user_factory.create(last_name=None)

        assert str(error.value) == errors["last_name"]["required"]

    def test_create_user_without_email_fails(self, user_factory):
        with pytest.raises(ValueError) as error:
            user_factory.create(email=None)

        assert str(error.value) == errors["email"]["required"]

    def test_create_user_with_invalid_email_fails(self, user_factory):
        with pytest.raises(ValueError) as error:
            user_factory.create(email="email")

        assert str(error.value) == errors["email"]["invalid"]

    def test_create_user_without_password_fails(self, user_factory):
        with pytest.raises(ValueError) as error:
            user_factory.create(password=None)

        assert str(error.value) == errors["password"]["required"]
