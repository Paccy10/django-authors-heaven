from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ..common.models import BaseModel
from .managers import UserManager

AUTH_PROVIDERS = {
    "facebook": "facebook",
    "google": "google",
    "twitter": "twitter",
    "email": "email",
}


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model"""

    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    auth_provider = models.CharField(
        max_length=100, blank=False, null=False, default=AUTH_PROVIDERS.get("email")
    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return f"{self.first_name}{f' {self.middle_name }'if self.middle_name else ''} {self.last_name}"
