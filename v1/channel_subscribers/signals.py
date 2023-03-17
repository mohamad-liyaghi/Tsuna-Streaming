from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete

from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber


def create_subscriber_after_creating_channel(sender, **kwargs):
    '''Create a subscriber for admin to a channel when its created.'''

    if kwargs["created"]:
        instance = kwargs["instance"]
        ChannelSubscriber.objects.create(channel=instance, user=instance.owner)
