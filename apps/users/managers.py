from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .error_messages import errors


class UserManager(BaseUserManager):
    """Custom user manager"""

    def email_validator(self, email):
        if not email:
            raise ValueError(errors["email"]["required"])

        email = self.normalize_email(email)

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(errors["email"]["invalid"])

    def validate_user_data(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(errors["username"]["required"])

        if not extra_fields["first_name"]:
            raise ValueError(errors["first_name"]["required"])

        if not extra_fields["last_name"]:
            raise ValueError(errors["last_name"]["required"])

        self.email_validator(email)

        if not password:
            raise ValueError(errors["password"]["required"])

    def create_user(self, username, email, password, **extra_fields):
        """Create and save a normal user"""

        self.validate_user_data(username, email, password, **extra_fields)

        user = self.model(username=username, email=email, **extra_fields)

        user.set_password(password)
        user.is_active = False
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a superuser"""

        user = self.create_user(username, email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
