import factory
from faker import Factory as FakerFactory

from apps.users.models import User

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""

    username = factory.LazyAttribute(lambda x: faker.first_name())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    middle_name = factory.LazyAttribute(lambda x: "")
    email = factory.LazyAttribute(lambda x: "test@example.com")
    password = factory.LazyAttribute(lambda x: "password")

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class ActiveUserFactory(factory.django.DjangoModelFactory):
    """Active User factory"""

    username = factory.LazyAttribute(lambda x: faker.first_name())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    middle_name = factory.LazyAttribute(lambda x: "")
    email = factory.LazyAttribute(lambda x: "active@example.com")
    password = factory.LazyAttribute(lambda x: "password")

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)
