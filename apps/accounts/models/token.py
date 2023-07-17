from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils import timezone
import datetime
from datetime import timedelta
from core.models import AbstractToken
from accounts.managers import VerificationTokenManager


class VerificationToken(AbstractToken):
    """
    This model is used to store the verification token for users
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_tokens",
    )

    expire_at = models.DateTimeField(null=True, blank=True)

    objects = VerificationTokenManager()

    def __str__(self) -> str:
        return f"{self.user} - {self.token}"

    @property
    def is_valid(self) -> bool:
        """
        Each token is valid for 10 minutes
        Return True if the token is valid
        """
        now = timezone.now()
        ten_minutes_ago = now - timedelta(minutes=10)
        return self.expire_at > ten_minutes_ago

    def save(self, *args, **kwargs):
        """
        Ovrride the save method for:
        - set the expiration date
        """
        if not self.expire_at:
            self.__check_user_active()
            self.__check_token_existance()
            self.__set_expiration_date()
        return super().save(*args, **kwargs)

    def __set_expiration_date(self) -> None:
        self.expire_at = timezone.now() + datetime.timedelta(minutes=10)

    def __check_token_existance(self) -> None:
        """
        Check if an active token already exists
        """

        verification_token = self.user.verification_tokens.first()

        if verification_token and verification_token.is_valid:
            raise PermissionDenied("An active token already exists.")

    def __check_user_active(self) -> None:
        """
        Check if the user is active
        """
        if self.user.is_active:
            raise ValidationError("User is already active.")

    class Meta:
        """
        Override the default ordering
        """
        ordering = ["expire_at"]
