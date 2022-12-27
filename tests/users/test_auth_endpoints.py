import datetime
import json
from time import sleep
from unittest.mock import MagicMock, patch

import django_rq
import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.error_messages import errors
from apps.users.models import AUTH_PROVIDERS
from authors_heaven.settings.base import env
from tests.constants import JSON_CONTENT_TYPE


@pytest.mark.django_db
class TestUserSignupEndpoint:
    """Test user signup endpoint"""

    url = reverse("signup")
    data = {
        "first_name": "Test",
        "last_name": "USer",
        "email": "test.user@app.com",
        "username": "test1",
        "password": "Password@1234",
    }

    def test_user_signup_succeeds(self, api_client):
        django_rq.enqueue = MagicMock(return_value=None)

        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 201
        assert response.json()["email"] == self.data["email"]
        assert response.json()["is_active"] is False

    def test_user_signup_without_first_name_fails(self, api_client):
        data = self.data.copy()
        data.pop("first_name")
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["required"]]

    def test_user_signup_with_blank_first_name_fails(self, api_client):
        data = self.data.copy()
        data["first_name"] = ""
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["first_name"] == [errors["first_name"]["blank"]]

    def test_user_signup_without_last_name_fails(self, api_client):
        data = self.data.copy()
        data.pop("last_name")
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["required"]]

    def test_user_signup_with_blank_last_name_fails(self, api_client):
        data = self.data.copy()
        data["last_name"] = ""
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["last_name"] == [errors["last_name"]["blank"]]

    def test_user_signup_without_username_fails(self, api_client):
        data = self.data.copy()
        data.pop("username")
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["username"] == [errors["username"]["required"]]

    def test_user_signup_with_blank_username_fails(self, api_client):
        data = self.data.copy()
        data["username"] = ""
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["username"] == [errors["username"]["blank"]]

    def test_user_signup_with_taken_username_fails(self, api_client, base_user):
        data = self.data.copy()
        data["username"] = base_user.username
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 409
        assert response.json()["detail"] == errors["username"]["unique"]

    def test_user_signup_without_email_fails(self, api_client):
        data = self.data.copy()
        data.pop("email")
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["required"]]

    def test_user_signup_with_blank_email_fails(self, api_client):
        data = self.data.copy()
        data["email"] = ""
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["blank"]]

    def test_user_signup_with_taken_email_fails(self, api_client, base_user):
        data = self.data.copy()
        data["email"] = base_user.email
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 409
        assert response.json()["detail"] == errors["email"]["unique"]

    def test_user_signup_without_password_fails(self, api_client):
        data = self.data.copy()
        data.pop("password")
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["password"] == [errors["password"]["required"]]

    def test_user_signup_with_blank_password_fails(self, api_client):
        data = self.data.copy()
        data["password"] = ""
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["password"] == [errors["password"]["blank"]]

    def test_user_signup_with_weak_password_fails(self, api_client):
        data = self.data.copy()
        data["password"] = "hello"
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["password"] == [
            errors["password"]["weak"],
            errors["password"]["min_length"],
        ]


@pytest.mark.django_db
class TestUserVerificationEndpoint:
    """Test user verification endpoint"""

    url = reverse("verify")

    def test_user_verification_succeeds(self, api_client, base_user):
        token = RefreshToken.for_user(base_user).access_token
        response = api_client.get(
            f"{self.url}?token={str(token)}", content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is True

    def test_user_verification_with_invalid_token_fails(self, api_client, base_user):
        response = api_client.get(
            f"{self.url}?token=token", content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["token"] == [errors["token"]["invalid"]]

    def test_user_verification_with_expired_token_fails(self, api_client, base_user):
        token = RefreshToken.for_user(base_user).access_token
        token.set_exp(lifetime=datetime.timedelta(seconds=1))
        sleep(2)
        response = api_client.get(
            f"{self.url}?token={str(token)}", content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["token"] == [errors["token"]["expired"]]


@pytest.mark.django_db
class TestUserLoginEndpoint:
    """Test user login endpoint"""

    url = reverse("login")

    def test_user_login_with_email_succeeds(self, api_client, active_user):
        data = {"email": active_user.email, "password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    def test_user_login_with_username_succeeds(self, api_client, active_user):
        data = {"username": active_user.username, "password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    def test_user_login_without_username_or_email_fails(self, api_client, base_user):
        data = {"password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["username"] == [errors["account"]["required"]]

    def test_user_login_without_password_fails(self, api_client, base_user):
        data = {"email": base_user.email}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["password"] == [errors["password"]["required"]]

    def test_user_login_with_wrong_email_fails(self, api_client, base_user):
        data = {"email": "baser_user@example.com", "password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json()["detail"] == errors["account"]["no_account"]

    def test_user_login_with_wrong_username_fails(self, api_client, base_user):
        data = {"username": "baser_user", "password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json()["detail"] == errors["account"]["no_account"]

    def test_user_login_with_wrong_password_fails(self, api_client, base_user):
        data = {"email": base_user.email, "password": "base_user.password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json()["detail"] == errors["account"]["no_account"]

    def test_user_login_with_inactivated_account_fails(self, api_client, base_user):
        data = {"email": base_user.email, "password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json()["detail"] == errors["account"]["disabled"]

    def test_user_login_with_different_provider_fails(self, api_client, base_user):
        base_user.auth_provider = AUTH_PROVIDERS.get("google")
        base_user.save()
        data = {"email": base_user.email, "password": "password"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json()["detail"] == errors["account"]["provider"].format(
            base_user.auth_provider
        )


@pytest.mark.django_db
class TestForgotPasswordEndpoint:
    """Test forgot password endpoint"""

    url = reverse("forgot-password")

    def test_forgot_password_succeeds(self, api_client, active_user):
        django_rq.enqueue = MagicMock(return_value=None)
        data = {"email": active_user.email}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert (
            response.json()["detail"]
            == "Password reset link successfully sent. Please check your email to continue"
        )

    def test_forgot_password_without_email_fails(self, api_client):
        data = {}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["required"]]

    def test_forgot_password_with_blank_email_fails(self, api_client):
        data = {"email": ""}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["blank"]]

    def test_forgot_password_with_invalid_email_fails(self, api_client):
        data = {"email": "email"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["email"] == [errors["email"]["invalid"]]

    def test_forgot_password_with_unexisted_email_fails(self, api_client):
        data = {"email": "email@app.com"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 404
        assert response.json()["detail"] == "User with email 'email@app.com' not found"


@pytest.mark.django_db
class TestResetPasswordEndpoint:
    """Test reset password endpoint"""

    url = reverse("reset-password")
    data = {"password": "Password@12345", "confirm_password": "Password@12345"}

    def test_reset_password_succeeds(self, api_client, active_user):
        token = RefreshToken.for_user(active_user).access_token
        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token={str(token)}", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 200
        assert response.json()["email"] == active_user.email

    def test_reset_password_without_password_fails(self, api_client):
        data = self.data.copy()
        data.pop("password")
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["password"] == [errors["password"]["required"]]

    def test_reset_password_with_blank_password_fails(self, api_client):
        data = self.data.copy()
        data["password"] = ""
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["password"] == [errors["password"]["blank"]]

    def test_reset_password_with_weak_password_fails(self, api_client):
        data = self.data.copy()
        data["password"] = "hello"
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["password"] == [
            errors["password"]["weak"],
            errors["password"]["min_length"],
        ]

    def test_reset_password_without_confirm_password_fails(self, api_client):
        data = self.data.copy()
        data.pop("confirm_password")
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["confirm_password"] == [
            errors["confirm_password"]["required"]
        ]

    def test_reset_password_with_blank_confirm_password_fails(self, api_client):
        data = self.data.copy()
        data["confirm_password"] = ""
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["confirm_password"] == [
            errors["confirm_password"]["blank"]
        ]

    def test_reset_password_with_unmatched_passwords_fails(self, api_client):
        data = self.data.copy()
        data["confirm_password"] = "Password@1234"
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["passwords"] == [errors["confirm_password"]["invalid"]]

    def test_reset_password_with_invalid_token_fails(self, api_client, base_user):
        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token=token", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["token"] == [errors["token"]["invalid"]]

    def test_reset_password_with_expired_token_fails(self, api_client, base_user):
        token = RefreshToken.for_user(base_user).access_token
        token.set_exp(lifetime=datetime.timedelta(seconds=1))
        sleep(2)
        data = self.data.copy()
        data = json.dumps(data)
        response = api_client.post(
            f"{self.url}?token={str(token)}", data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["token"] == [errors["token"]["expired"]]


@pytest.mark.django_db
class TestGoogleAuthEndpoint:
    """Test google auth endpoint"""

    url = reverse("google-auth")

    @patch("google.oauth2.id_token.verify_token", autospec=True)
    def test_google_auth_succeeds(self, verify_token, api_client):
        verify_token.return_value = {
            "iss": "accounts.google.com",
            "email": "test.user@app.com",
            "name": "test user",
            "given_name": "test",
            "family_name": "user",
            "aud": env("GOOGLE_CLIENT_ID"),
        }

        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()

    @patch("google.oauth2.id_token.verify_token", autospec=True)
    def test_google_auth_with_existing_username_succeeds(
        self, verify_token, api_client, active_user
    ):
        active_user.username = active_user.username.lower()
        active_user.save()

        verify_token.return_value = {
            "iss": "accounts.google.com",
            "email": "test.user@app.com",
            "name": f"{active_user.username}",
            "given_name": "test",
            "family_name": "user",
            "aud": env("GOOGLE_CLIENT_ID"),
        }

        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()

    @patch("google.oauth2.id_token.verify_token", autospec=True)
    def test_google_auth_with_existing_user_succeeds(
        self, verify_token, api_client, active_user
    ):
        verify_token.return_value = {
            "iss": "accounts.google.com",
            "email": active_user.email,
            "name": "test user",
            "given_name": "test",
            "family_name": "user",
            "aud": env("GOOGLE_CLIENT_ID"),
        }

        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_google_auth_with_invalid_id_token_fails(self, api_client):
        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["auth_token"] == [errors["token"]["invalid"]]

    @patch("google.oauth2.id_token.verify_token", autospec=True)
    def test_google_auth_invalid_client_id_fails(
        self, verify_token, api_client, active_user
    ):
        verify_token.return_value = {
            "iss": "accounts.google.com",
            "email": active_user.email,
            "name": "test user",
            "given_name": "test",
            "family_name": "user",
            "aud": "GOOGLE_CLIENT_ID",
        }

        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json()["detail"] == errors["social_app_id"]["invalid"]


@pytest.mark.django_db
class TestFacebbokAuthEndpoint:
    """Test facebook auth endpoint"""

    url = reverse("facebook-auth")

    @patch("facebook.GraphAPI.request", autospec=True)
    def test_facebook_auth_succeeds(self, request, api_client):
        request.return_value = {
            "email": "test.user@app.com",
            "name": "test user",
            "first_name": "test",
            "last_name": "user",
        }

        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_facebook_auth_with_invalid_access_token_fails(self, api_client):
        data = {"auth_token": "auth_token"}
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["auth_token"] == [errors["token"]["invalid"]]


@pytest.mark.django_db
class TestTwitterAuthEndpoint:
    """Test twitter auth endpoint"""

    url = reverse("twitter-auth")

    def test_twitter_auth_succeeds(self, api_client):
        data = {
            "access_token_key": env("TWITTER_ACCESS_TOKEN_KEY"),
            "access_token_secret": env("TWITTER_ACCESS_TOKEN_SECRET"),
        }
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_twitter_auth_with_invalid_access_tokens_fails(self, api_client):
        data = {
            "access_token_key": "access_token_key",
            "access_token_secret": "access_token_secret",
        }
        data = json.dumps(data)
        response = api_client.post(self.url, data=data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json()["access_tokens"] == [errors["access_tokens"]["invalid"]]
