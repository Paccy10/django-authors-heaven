import pytest
from django.urls import reverse


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
