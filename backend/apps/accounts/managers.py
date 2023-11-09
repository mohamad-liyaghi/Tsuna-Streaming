from django.shortcuts import get_object_or_404
from django.contrib.auth.models import BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(self, email: str, password: str, is_active=False, **kwargs):
        """
        Override the create_user method to create a user with a given email and password
        """
        email = self.normalize_email(email)

        user = self.model(email=email, is_active=is_active, **kwargs)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        """Create a superuser"""
        email = self.normalize_email(email)

        user = self.model(
            email=email, is_active=True, is_superuser=True, is_staff=True, **kwargs
        )

        user.set_password(password)
        user.save()
        return user


class VerificationTokenManager(models.Manager):
    """Custom manager for verification tokens"""

    def verify(self, user: "Account", token: "VerificationToken"):
        """
        Check user is not active and the code is valid
        """

        if user.is_active:
            return False, "User is already active."

        if token.user != user:
            return False, "Token and user mismath."

        if not token.is_valid:
            return False, "Token is expired."

        return True, "ok"
