import json

import pytest
from django.urls import reverse

from tests.constants import JSON_CONTENT_TYPE


@pytest.mark.django_db
class TestCreateArticleEndpoint:
    """Test create new article endpoint"""

    url = reverse("all-articles")
    data = {"title": "article 1", "body": "article 1 body", "tags": ["tag1", "tag2"]}

    def test_create_article_with_unauthorized_user_fails(self, auth_api_client):
        auth_api_client.credentials()
        data = self.data.copy()
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_create_article_succeeds(self, auth_api_client):
        data = self.data.copy()
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 201
        assert response.json()["title"] == self.data["title"]
        assert response.json()["body"] == self.data["body"]

    def test_create_article_without_title_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("title")
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["title"] == ["This field is required."]

    def test_create_article_with_blank_title_fails(self, auth_api_client):
        data = self.data.copy()
        data["title"] = ""
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["title"] == ["This field may not be blank."]

    def test_create_article_with_null_title_fails(self, auth_api_client):
        data = self.data.copy()
        data["title"] = None
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["title"] == ["This field may not be null."]

    def test_create_article_without_body_fails(self, auth_api_client):
        data = self.data.copy()
        data.pop("body")
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["body"] == ["This field is required."]

    def test_create_article_with_blank_body_fails(self, auth_api_client):
        data = self.data.copy()
        data["body"] = ""
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["body"] == ["This field may not be blank."]

    def test_create_article_with_null_body_fails(self, auth_api_client):
        data = self.data.copy()
        data["body"] = None
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 400
        assert response.json()["body"] == ["This field may not be null."]

    def test_article_has_different_slug_succeeds(self, auth_api_client, base_article):
        data = self.data.copy()
        data["title"] = base_article.title
        data = json.dumps(data)
        response = auth_api_client.post(
            self.url, data=data, content_type=JSON_CONTENT_TYPE
        )

        assert response.status_code == 201
        assert response.json()["slug"] != base_article.slug
