import json

import pytest
from django.urls import reverse

from apps.users.models import User
from tests.constants import JSON_CONTENT_TYPE

from ..utils import get_dynamic_url


@pytest.mark.django_db
class TestGetMyProfileEndpoint:
    """Test get my profile endpoint"""

    url = reverse("my-profile")

    def test_get_my_profile_with_unauthorized_user_fails(self, auth_api_client):
        auth_api_client.credentials()
        response = auth_api_client.get(self.url)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_my_profile_succeeds(self, auth_api_client):
        response = auth_api_client.get(self.url)

        assert response.status_code == 200
        assert response.json()["email"] == "active@example.com"


@pytest.mark.django_db
class TestEditMyProfileEndpoint:
    """Test edit my profile endpoint"""

    url = reverse("my-profile")
    data = {
        "first_name": "Test",
        "last_name": "User",
        "middle_name": "Another",
        "phone_number": "+250780000000",
        "about_me": "About me",
        "gender": "Other",
        "country": "Rwanda",
        "city": "Kigali",
    }

    def test_edit_my_profile_with_unauthorized_user_fails(self, auth_api_client):
        auth_api_client.credentials()
        data = self.data.copy()
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_edit_my_profile_succeeds(self, auth_api_client):
        data = self.data.copy()
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 200
        assert response.json()["middle_name"] == self.data["middle_name"]

    def test_edit_my_profile_without_first_name_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("first_name")
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["first_name"] == ["This field is required."]

    def test_edit_my_profile_with_blank_first_name_fails(self, auth_api_client):
        data = self.data.copy()
        data["first_name"] = ""
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["first_name"] == ["This field may not be blank."]

    def test_edit_my_profile_without_last_name_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("last_name")
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["last_name"] == ["This field is required."]

    def test_edit_my_profile_with_blank_last_name_fails(self, auth_api_client):
        data = self.data.copy()
        data["last_name"] = ""
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["last_name"] == ["This field may not be blank."]

    def test_edit_my_profile_without_phone_number_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("phone_number")
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["phone_number"] == ["This field is required."]

    def test_edit_my_profile_with_blank_phone_number_fails(self, auth_api_client):
        data = self.data.copy()
        data["phone_number"] = ""
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["phone_number"] == ["This field may not be blank."]

    def test_edit_my_profile_with_invalid_phone_number_fails(self, auth_api_client):
        data = self.data.copy()
        data["phone_number"] = "33434"
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["phone_number"] == ["Enter a valid phone number."]

    def test_edit_my_profile_without_about_me_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("about_me")
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["about_me"] == ["This field is required."]

    def test_edit_my_profile_with_blank_about_me_fails(self, auth_api_client):
        data = self.data.copy()
        data["about_me"] = ""
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["about_me"] == ["This field may not be blank."]

    def test_edit_my_profile_without_gender_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("gender")
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["gender"] == ["This field is required."]

    def test_edit_my_profile_with_invalid_gender_fails(self, auth_api_client):
        data = self.data.copy()
        invalid_gender = "dsdsd"
        data["gender"] = invalid_gender
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["gender"] == [
            f'"{invalid_gender}" is not a valid choice.'
        ]

    def test_edit_my_profile_without_country_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("country")
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["country"] == ["This field is required."]

    def test_edit_my_profile_with_invalid_country_fails(self, auth_api_client):
        data = self.data.copy()
        invalid_country = "dsdsd"
        data["country"] = invalid_country
        data = json.dumps(data)
        response = auth_api_client.put(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["country"] == [
            f'"{invalid_country}" is not a valid choice.'
        ]


@pytest.mark.django_db
class TestGetUserProfileEndpoint:
    """Test get another user profile endpoint"""

    def test_get_user_profile_with_unauthorized_user_fails(self, auth_api_client):
        url = get_dynamic_url(User, "user-profile")
        auth_api_client.credentials()

        response = auth_api_client.get(url)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_user_profile_succeeds(self, auth_api_client):
        url = get_dynamic_url(User, "user-profile")
        response = auth_api_client.get(url)

        assert response.status_code == 200

    def test_get_user_profile_with_unexisted_id_fails(self, admin_api_client):
        url = reverse("user-profile", args=["sdfdd"])
        response = admin_api_client.get(url)

        assert response.status_code == 404
        assert response.json()["detail"] == "Not found."
