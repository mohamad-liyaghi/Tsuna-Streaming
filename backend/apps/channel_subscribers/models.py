from django.db import models
from django.conf import settings
from channels.models import Channel
from channel_subscribers.managers import ChannelSubscriberManager


class ChannelSubscriber(models.Model):
    """Model to represent a user's subscription to a channel."""

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="subscribers"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribed_channels"
    )

    date = models.DateTimeField(auto_now_add=True)
    objects = ChannelSubscriberManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_subscribers"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} subscribed to {self.channel}"
