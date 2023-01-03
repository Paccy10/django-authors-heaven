import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..factories.article import ArticleFactory

register(ArticleFactory)


@pytest.fixture
def base_article(db, article_factory):
    new_article = article_factory.create()
    return new_article
