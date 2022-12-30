import pytest
from django.urls import reverse
from ..utils import get_dynamic_url
from apps.users.models import User


@pytest.mark.django_db
class TestGetUsersEndpoint:
    """Test get users endpoint"""

    url = reverse("get-users")

    def test_get_users_with_unauthorized_user_fails(self, auth_api_client):
        auth_api_client.credentials()
        response = auth_api_client.get(self.url)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_users_without_permissions_fails(self, auth_api_client):
        response = auth_api_client.get(self.url)

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_get_users_succeeds(self, admin_api_client, base_user):
        response = admin_api_client.get(self.url)

        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.django_db
class TestGetUserEndpoint:
    """Test get user endpoint"""

    def test_get_user_with_unauthorized_user_fails(self, auth_api_client):
        auth_api_client.credentials()
        url = get_dynamic_url(User, "get-user")
        response = auth_api_client.get(url)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_user_without_permissions_fails(self, auth_api_client):
        url = get_dynamic_url(User, "get-user")
        response = auth_api_client.get(url)

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "You do not have permission to perform this action."
        )

    def test_get_user_succeeds(self, admin_api_client):
        url = get_dynamic_url(User, "get-user")
        response = admin_api_client.get(url)

        assert response.status_code == 200
        assert response.json()["email"] == "active@example.com"
