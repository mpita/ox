"""Account Models."""
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField


class UserManager(BaseUserManager):
    """Account user manager."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a User with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")

        extra_fields.pop("username", None)

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and saves a superuser with the given email and password."""
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    """Account user models."""

    avatar = VersatileImageField(upload_to="avatar", blank=True, null=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )
    first_name = models.CharField(_("first name"), max_length=256, blank=True)
    last_name = models.CharField(_("last name"), max_length=256, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        """Meta user model."""

        ordering = (
            "email",
            "last_name",
        )

    def __str__(self):
        """Get email user."""
        return self.email

    def get_full_name(self):
        """Get full name user."""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    def get_short_name(self):
        """Get full name user."""
        return self.email
