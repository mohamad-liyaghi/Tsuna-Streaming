from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(
            self, email: str, password: str, is_active=False, **kwargs
    ):
        """
        Override the create_user method to create a user with a given email and password
        """
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_active=is_active,
            **kwargs
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        """Create a superuser"""
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_active=True,
            is_superuser=True,
            is_staff=True,
            **kwargs
        )

        user.set_password(password)
        user.save()
        return user
