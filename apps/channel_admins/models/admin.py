from django.db import models
from django.conf import settings
from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber
from django.core.exceptions import PermissionDenied
from channel_admins.exceptions import (
    SubscriptionRequiredException
)
from core.models import AbstractToken


class ChannelAdmin(AbstractToken):
    """
    Represents a channel admin.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='channel_admins'
    )
    promoted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='promoted_admins',
        blank=True, null=True,
    )

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='admins'
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)
    
    class Meta:
        # unique together with channel and user
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_admin"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.pk:

            # Check user subscription status
            ChannelAdmin.check_promoter_status(channel=self.channel, user=self.user)

            # Check if user can be promoted
            ChannelAdmin.check_promotion_permission(
                channel=self.channel, user=self.user, promoter=self.promoted_by
            )

        return super(ChannelAdmin, self).save(*args, **kwargs)

    @classmethod
    def check_subscription(cls, channel, user) -> None:
        """
        Check user has subscribed or not.
        If user has subscribed, check if he has subscribed for at least 24 hours.
        """
        subscriber = ChannelSubscriber.objects.get_from_cache(
                    channel=channel, user=user
        )

        # Raise error if use hasnt subscribed to channel
        if not subscriber:
            raise SubscriptionRequiredException(
                "User hasnt subscribed to channel."
            )

        if subscriber and not ChannelSubscriber.objects.filter(channel=channel, user=user):
            raise SubscriptionRequiredException(
                "User must be subscribed to channel for at least 24 hours to get promoted."
            )

    @classmethod
    def check_promoter_status(cls, channel, user, promoter=None) -> None:
        """
        Check if promoter is the channel owner
        """
        if user == promoter:
            return

        if not promoter == channel.owner:
            raise PermissionDenied("Only Channel Owners can add/del admins.")
