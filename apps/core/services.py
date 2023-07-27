from django.db import models
from django.core.cache import cache
from django.conf import settings
from typing import Union
from datetime import datetime
from channels.models import Channel
from core.utils import ObjectSource


class CacheService:
    """
    A service which provides methods for working with cache.
    List/Get/Set/Update/Delete objects in cache.
    """
    def __init__(self, model: models.Model):
        self.model = model

    def get_list(
            self, *,
            key: str,
            channel: Channel,
    ) -> Union[list, int]:
        """
        Return List of objects from cache and db
        Args:
            key: str
            channel: Channel
        """
        # Objects from cache
        objects_in_cache = [
            cache.get(object_key) for object_key in cache.keys(key)
        ]

        # objects with source of cache
        cache_objects = list(
            filter(
                lambda obj: obj.get('source') == ObjectSource.CACHE.value and not obj.get('pending_delete'),
                objects_in_cache
            )
        )

        # Objects from db
        db_objects = list(
            self.model.objects.filter(channel=channel).values(
                'user', 'channel', 'date'
            )
        )
        # return cached_objects + db_objects
        return cache_objects + db_objects

    def get_from_cache(
            self, *,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            exists: bool = False
    ) -> Union[dict, None]:
        """
        Return object from cache or db or check if object exists in cache or db
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
            exists: bool - if True, check if object exists in cache or db
        """
        # Search in db for object
        object_in_db = self.__search_in_db(key=key, channel=channel, user=user)
        # Search in cache for object
        object_in_cache = self.__search_in_cache(key=key, channel=channel, user=user)

        if object_in_cache and object_in_cache.get('pending_delete'):
            return

        # If user wants to check if object exists in cache or db, return True or False
        if exists:
            return object_in_db or object_in_cache

        # If object is in DB, return it
        if object_in_db:
            return object_in_db

        # If object is in cache, return it
        if object_in_cache:
            return object_in_cache

        return

    def create_cache(
            self, *,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            **data
    ) -> Union[dict, None]:
        """
        Create a new object in cache (if not exist)
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
            **data: dict - Extra data
        """

        # First check if object exists in cache or db
        # If exists, return None
        if self.get_from_cache(key=key, channel=channel, user=user, exists=True):
            return

        # If not exist, create a new object in cache
        return self.__set_cache(
            key=key,
            channel=channel,
            user=user,
            **data
        )

    def delete_cache(
            self, *,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
    ) -> Union[dict, None]:
        """
        Delete object from cache
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        get_cache = self.get_from_cache(key=key, channel=channel, user=user)
        # First check if object exists in cache or db
        # If not exists, return None
        if not get_cache:
            raise ValueError("Object does not exist in cache or db.")

        if get_cache.get('source') == ObjectSource.DATABASE.value:
            self.__set_cache(
                key=key,
                channel=channel,
                user=user,
                pending_delete=True
            )
            return

        # If exists, delete object from cache
        cache.delete(key)
        return

    def __search_in_cache(
            self,
            key: str,
            user: settings.AUTH_USER_MODEL,
            channel: Channel
    ) -> Union[list, None]:
        """
        Search for object in cache
        """
        # Get object from cache
        cache_object = cache.get(key)

        # If object exists in cache, return it
        if cache_object is not None:
            return cache_object
        # Otherwise, return None
        return

    def __search_in_db(
            self,
            key: str,
            user: settings.AUTH_USER_MODEL,
            channel: Channel
    ) -> Union[dict, None]:
        cached_object = cache.get(key)

        if not cached_object:
            # Check if object exists in db
            obj = self.model.objects.filter(
                user=user,
                channel=channel
            )
            # Set object in cache and return it
            if obj.exists():
                return self.__set_cache(
                    key=key,
                    channel=channel,
                    user=user,
                    source=ObjectSource.DATABASE.value,
                )

            # Return none if object does not exist in db
            return

        return cached_object

    def __set_cache(
            self,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            source: str = ObjectSource.CACHE.value,
            date: datetime = datetime.now(),
            pending_delete: bool = False,
            **extra_data
    ) -> dict:
        """
        Set a record in cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            source: str
            date: datetime
            **extra_data: dict - Extra data
        """
        cache.set(
            key=key,
            value={
                'user': user.id,
                'channel': channel.id,
                'source': source,
                'date': date,
                'pending_delete': pending_delete,
                **extra_data
            },
            timeout=60
        )
        return cache.get(key)
