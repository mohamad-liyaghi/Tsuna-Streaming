from django.db import models
from django.conf import settings
from typing import Union
from channels.models import Channel
from core.utils import ObjectSource
from channel_subscribers.services import ChannelSubscriberService
from channel_subscribers.constants import CACHE_SUBSCRIBER_KEY


class ChannelSubscriberManager(models.Manager):
    """
    A manager for subscriber model which uses Subscriber Service for
    CRUD operations in cache
    """

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
        return len(self.service.get_list(key=CACHE_SUBSCRIBER_KEY, channel=channel))

    def get_list(self, channel: Channel) -> dict:
        """
        Get list of subscribers from cache and db.
        """
        return self.service.get_list(
            key=CACHE_SUBSCRIBER_KEY,
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
        return self.service.get_from_cache(
            key=CACHE_SUBSCRIBER_KEY,
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
        return self.service.create_cache(
            key=CACHE_SUBSCRIBER_KEY,
            channel=channel,
            user=user,
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
        return self.service.delete_cache(
            key=CACHE_SUBSCRIBER_KEY,
            channel=channel,
            user=user,
        )
