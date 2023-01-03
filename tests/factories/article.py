import factory
from faker import Factory as FakerFactory

from apps.articles.helpers.utils import generate_slug
from apps.articles.models import Article

faker = FakerFactory.create()


class ArticleFactory(factory.django.DjangoModelFactory):
    """Article factory"""

    title = factory.LazyAttribute(lambda x: "new-title")
    body = factory.LazyAttribute(lambda x: faker.paragraph(nb_sentences=5))
    slug = factory.LazyAttribute(lambda x: generate_slug(x.title))
    tags = factory.LazyAttribute(lambda x: ["tag1", "tag2"])
    author = factory.SubFactory("tests.factories.user.UserFactory")

    class Meta:
        model = Article
