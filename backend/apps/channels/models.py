from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from accounts.validators import validate_profile_size
from channels.exceptions import ChannelLimitExceededException
from core.models import AbstractToken


class Channel(AbstractToken):
    
    title = models.CharField(max_length=240)
    description = models.TextField(
        max_length=500,
        default="A new channel on Tsuna Streaming."
    )

    avatar = models.ImageField(
        upload_to="channels/profile",
        default="assets/images/default-channel-profile.jpg",
        validators=[validate_profile_size]
    )

    thumbnail = models.ImageField(
        upload_to="channels/profile",
        default="assets/images/default-thumbnail.jpg",
        validators=[validate_profile_size]
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="channels"
    )

    date_created = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        
        if not self.pk:
            self.__check_user_activation()
            self.__check_channel_limit()

        return super(Channel, self).save(*args, **kwargs)

    def __check_user_activation(self) -> None:
        """
        Checks if the user is active.
        """
        if not self.owner.is_active:
            raise PermissionDenied("User is not active.")

    def __check_channel_limit(self) -> None:
        """
        Checks if the user has reached the maximum allowed number of channels.

        - Admins have unlimited channels
        - Premium users can create up to 10 channels
        - Normal users can create up to 5 channels
          - If a normal user was previously premium and created > 5 channels,
            they can still create up to 10 channels.
        """

        if self.owner.is_admin():
            return

        max_channels = 10 if self.owner.is_premium() else 5
        user_channel_count = self.owner.channels.count()

        # If a user has created more than 5 channels, it means it has been premium
        # before. So we allow them to create up to 10 channels.
        if 10 > user_channel_count > 5 or user_channel_count < max_channels:
            return

        raise ChannelLimitExceededException(
            "User has reached the maximum number of channels."
        )

    def __str__(self) -> str:
        return self.title
