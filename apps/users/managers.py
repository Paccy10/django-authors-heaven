from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .error_messages import errors


class UserManager(BaseUserManager):
    """Custom user manager"""

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(errors["email"]["invalid"])

    def create_user(
        self, username, first_name, last_name, email, password, **extra_fields
    ):
        """Create and save a normal user"""

        if not username:
            raise ValueError(errors["username"]["required"])

        if not first_name:
            raise ValueError(errors["first_name"]["required"])

        if not last_name:
            raise ValueError(errors["last_name"]["required"])

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(errors["email"]["required"])

        if not password:
            raise ValueError(errors["password"]["required"])

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, first_name, last_name, email, password, **extra_fields
    ):
        """Create and save a superuser"""

        user = self.create_user(
            username, first_name, last_name, email, password, **extra_fields
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
