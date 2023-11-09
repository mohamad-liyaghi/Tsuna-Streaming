from django.db import models
from django.conf import settings
from typing import Union
from channels.models import Channel
from core.utils import ObjectSource


class BaseCacheManager(models.Manager):
    """
    Base cache manager for performing cache operations.
    This manager is abstract and can be used within other managers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = None

    def contribute_to_class(self, model, name):
        """
        Set service and cache key.
        """
        super().contribute_to_class(model, name)
        self.service = None

    def get_count(self, channel: Channel, **kwargs) -> int:
        """
        Return Number of objects for a channel (Could be cached or db)
        Eg: Number of subscribers for a channel
        args:
            channel: Channel
            Extra: Could be any extra info such as the object token
        """
        return len(self.service.get_list(channel=channel, **kwargs))

    def get_list(self, channel: Channel, **kwargs) -> dict:
        """
        List of an object for a channel (Could be cached or db).
        Eg: List of subscribers for a channel
        args:
            channel: Channel
            Extra: Could be any extra info such as the object token
        """
        return self.service.get_list(channel=channel, **kwargs)

    def get_from_cache(
        self, channel: Channel, user: settings.AUTH_USER_MODEL, **kwargs
    ) -> Union[dict, None]:
        """
        Get an object from cache or db
        Eg: Get a subscriber from cache or db
        args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            Extra: Could be any extra info such as the object token
        """
        return self.service.get_from_cache(channel=channel, user=user, **kwargs)

    def create_in_cache(
        self, channel: Channel, user: settings.AUTH_USER_MODEL, **kwargs
    ) -> Union[dict, None]:
        """
        Create an object in cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            Extra: Could be any extra info such as the object token
        """
        return self.service.create_cache(
            channel=channel, user=user, source=ObjectSource.CACHE.value, **kwargs
        )

    def delete_in_cache(
        self,
        channel: Channel,
        user: settings.AUTH_USER_MODEL,
        content_object: models.Model = None,
    ) -> None:
        """
        Delete an object from cache or db
        If object is saved in db, create a record in cache with
        perform_delete=True
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
        """
        return self.service.delete_cache(
            channel=channel, user=user, content_object=content_object
        )
