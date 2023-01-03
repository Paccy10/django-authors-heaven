from django.urls import reverse
from apps.articles.models import Article


def get_dynamic_url(model, url_name):
    instance = model.objects.first()
    url = reverse(url_name, args=[instance.id])

    return url


def get_article_dynamic_url():
    article = Article.objects.first()
    url = reverse("single-article", args=[article.slug])

    return url
