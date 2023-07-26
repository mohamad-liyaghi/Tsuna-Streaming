from channel_subscribers.models import ChannelSubscriber


def create_subscriber_after_creating_channel(sender, created, instance, **kwargs):
    """
    Create a new subscriber for channel owner after creating it
    """

    if created:
        ChannelSubscriber.objects.create(
            channel=instance,
            user=instance.owner
        )
