from django.db import models
from channels.models import Channel
from django.conf import settings


class ChannelSubscriber(models.Model):
    '''Channel Subscriber model'''
    
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="subscribers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="subscribed_channels")

    date = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_subscriber"
            )
        ]

    def __str__(self) -> str:
        return str(self.user)
