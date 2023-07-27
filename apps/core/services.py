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
    List/Get/Set/Delete objects in cache.
    """
    def __init__(self, model: models.Model):
        """
        Set the default model for the service
        """
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
        key = key.format(channel.token, "*")
        cached_result = cache.get(key)

        if cached_result is None:
            cache_objects = self.__get_all_from_cache(
                key=f"cached_{key}",
                object_key=key,
                channel=channel
            )
            db_objects = self.__get_all_from_db(key=f"db_{key}", channel=channel)

            # Combine cache and db objects
            combined_objects = cache_objects + db_objects

            unique_objects = self.__get_unique_objects(objects=combined_objects)

            cache.set(key, unique_objects, timeout=60)
            # Return the unique objects
            return unique_objects

        return cached_result

    def get_from_cache(
            self, *,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
    ) -> Union[dict, None]:
        """
        Return object from cache or db or check if object exists in cache or db
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        key = key.format(channel.token, user.token)
        # First search in db for the object
        search_in_db = self.__search_in_db(
            key=f"db_{key}", channel=channel, user=user
        )
        # Search in cache for object
        search_in_cache = self.__search_in_cache(key=key)

        # If object is pending delete, return None
        if search_in_cache and search_in_cache.get('pending_delete'):
                return

        # If object is in cache, return it
        if search_in_db:
            return search_in_db

        return search_in_cache

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
        key = key.format(channel.token, user.token)

        # First check if object exists in cache or db
        # If exists, return None
        if self.get_from_cache(key=key, channel=channel, user=user):
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
        key = key.format(channel.token, user.token)
        # First check if object exists in cache or db
        get_cache = self.get_from_cache(key=key, channel=channel, user=user)
        # If not exists, Raise exception
        if not get_cache:
            raise ValueError("Object does not exist in cache or db.")

        # If object is in db, do not delete the cache
        # Create a record which then celery would delete its object
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
    ) -> Union[list, None]:
        """
        Search for object in cache
        """
        return cache.get(key)

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

    def __get_all_from_cache(
            self, *,
            key: str,
            object_key: str,
            channel: Channel,
    ) -> list:
        """
        Return all objects that are only saved in cache
        """
        cached_result = cache.get(key)
        if cached_result is None:
            # Get all objects in cache
            caches = [
                cache.get(object_key) for object_key in cache.keys(object_key)
            ]

            # Filter objects that are only in cache, not saved in db
            cached_object = list(
                filter(
                    lambda obj: obj.get('source') == ObjectSource.CACHE.value,
                    caches
                )
            )
            cache.set(key, cached_object, timeout=60)
            return cached_object

        return cached_result

    def __get_all_from_db(
            self, *,
            key: str,
            channel: Channel,
    ) -> list:
        """
        Return all objects that are only saved in db
        """
        cached_result = cache.get(key)

        if cached_result is None:
            # Objects from db
            db_objects = list(
                self.model.objects.filter(channel=channel).values(
                    'user', 'channel', 'date'
                )
            )
            cache.set(key, db_objects, timeout=60)
            return db_objects

        return cached_result

    def __get_unique_objects(self, objects: list) -> list:
        # Remove duplicate users and check pending delete
        unique_objects = []
        seen_users = set()
        for combined_object in objects:
            user = combined_object.get('user')
            if user not in seen_users:
                if combined_object.get('pending_delete') is not True:
                    unique_objects.append(combined_object)
                seen_users.add(user)
        return unique_objects
