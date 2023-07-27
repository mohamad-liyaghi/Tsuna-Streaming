from django.db import models
from django.conf import settings
from typing import Union
from decouple import config
from channels.models import Channel
from core.utils import ObjectSource
from channel_subscribers.services import ChannelSubscriberService
from channel_subscribers.utils import SubscriberStatus

# COMMON CACHE KEYS
CACHE_SUBSCRIBER_KEY = config('CACHE_CHANNEL_SUBSCRIBER')
CACHE_UNSUBSCRIBER_COUNT_KEY = config('CACHE_CHANNEL_UNSUBSCRIBER_COUNT')
CACHE_DB_SUBSCRIBERS_COUNT_KEY = config('CACHE_CHANNEL_DB_SUBSCRIBERS_COUNT')


class ChannelSubscriberManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = None

    def contribute_to_class(self, model, name):
        super().contribute_to_class(model, name)
        self.service = ChannelSubscriberService(self.model)

    def get_count(self, channel: Channel) -> int:
        """
        Return number of subscribers for a channel.
        args:
            channel: Channel
        """

        key = CACHE_SUBSCRIBER_KEY.format(channel.token, "*")
        return len(self.service.get_list(key=key, channel=channel))

    def get_list(self, channel: Channel) -> dict:
        """
        Get list of subscribers from cache and db.
        """
        subscriber_key = CACHE_SUBSCRIBER_KEY.format(channel.token, '*')

        return self.service.get_list(
            key=subscriber_key,
            channel=channel
        )

    def get_from_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> Union[dict, None]:
        """
        Get subscriber from cache/db and return it.
        args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)
        return self.service.get_from_cache(
            key=key,
            channel=channel,
            user=user
        )

    def create_in_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> Union[dict, None]:
        """
        Create a subscriber in cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)

        return self.service.create_cache(
            key=key,
            channel=channel,
            user=user,
            subscription_status=SubscriberStatus.SUBSCRIBED.value,
            source=ObjectSource.CACHE.value
        )

    def delete_in_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> None:
        """
        Delete a subscriber from cache
        If subscriber is in db, create a record in cache with
        subscription_status = unsubscribed
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)
        return self.service.delete_cache(
            key=key,
            channel=channel,
            user=user,
        )
