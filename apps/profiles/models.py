import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from ..common.models import BaseModel

User = get_user_model()


def get_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return "profiles/{0}/{1}".format(instance.user.username, filename)


class Gender(models.TextChoices):
    Male = "Male", "Male"
    Female = "Female", "Female"
    Other = "Other", "Other"


class Profile(BaseModel):
    """Profile model"""

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=30, null=True)
    about_me = models.TextField(null=True)
    avatar = models.ImageField(upload_to=get_upload_to, null=True)
    gender = models.CharField(choices=Gender.choices, max_length=20, null=True)
    country = CountryField(null=True)
    city = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
