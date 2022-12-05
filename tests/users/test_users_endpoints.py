from apps.users.error_messages import errors
from django.urls import reverse
import json
from tests.constants import JSON_CONTENT_TYPE
import pytest


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
