import factory
from django.db.models.signals import post_save
from faker import Factory as FakerFatcory

from apps.profiles.models import Profile

faker = FakerFatcory.create()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """Profile factory"""

    user = factory.SubFactory("tests.factories.user.UserFactory")
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    about_me = factory.LazyAttribute(lambda x: faker.sentence(nb_words=10))
    avatar = factory.LazyAttribute(lambda x: faker.file_extension(category="image"))
    gender = factory.LazyAttribute(lambda x: "male")
    country = factory.LazyAttribute(lambda x: faker.country_code())
    city = factory.LazyAttribute(lambda x: faker.city())

    class Meta:
        model = Profile
