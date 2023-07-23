from django.dispatch import receiver
from django.db.models.signals import post_save

from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber


@receiver(post_save, sender=Channel)
def create_subscriber_after_creating_channel(sender, created, instance, **kwargs):
    """
    Create a new subscriber for channel owner after creating it
    """

    if created:
        ChannelSubscriber.objects.create(
            channel=instance,
            user=instance.owner
        )
