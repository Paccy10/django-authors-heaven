import datetime
import json
from time import sleep
from unittest.mock import MagicMock

import django_rq
import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.error_messages import errors
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
