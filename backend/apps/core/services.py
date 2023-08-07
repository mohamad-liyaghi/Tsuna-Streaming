from django.db import models
from django.core.cache import cache
from django.conf import settings
from typing import Union
from datetime import datetime
from channels.models import Channel
from core.utils import ObjectSource
from core.utils import get_content_type_model


class CacheService:
    """
    A service to handle cache operations.
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
            content_object: models.Model = None,
            **kwargs
    ) -> Union[list, int]:
        """
        Return List of objects from cache and db
        Args:
            key: str
            channel: Channel
            content_object: models.Model
            **kwargs: dict - Extra data
        """
        key = self.__generate_key(
            key=key,
            channel=channel,
            user='*',
            content_object=content_object
        )
        cached_result = cache.get(key)

        if cached_result is None:
            cache_objects = self.__get_all_from_cache(key=key)
            db_objects = self.__get_all_from_db(channel=channel, **kwargs)

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
            content_object: models.Model = None,
    ) -> Union[dict, None]:
        """
        Return object from cache or db or check if object exists in cache or db
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
        """
        key = self.__generate_key(
            key=key,
            channel=channel,
            user=user,
            content_object=content_object
        )
        # First search in db for the object
        search_in_db = self.__search_in_db(
            key=key, channel=channel, user=user, content_object=content_object
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
            content_object: models.Model = None,
            **kwargs
    ) -> Union[dict, None]:
        """
        Create a new object in cache (if not exist)
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
            **kwargs: dict - Extra data
        """
        key = self.__generate_key(
            key=key,
            channel=channel,
            user=user,
            content_object=content_object
        )

        # First check if object exists in cache or db
        # If exists, return None
        if self.get_from_cache(
                key=key,
                channel=channel,
                user=user,
                content_object=content_object
        ):
            return

        # If not exist, create a new object in cache
        return self.__set_cache(
            key=key,
            channel=channel,
            user=user,
            content_object=content_object,
            **kwargs
        )

    def delete_cache(
            self, *,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            content_object: models.Model = None,
            **kwargs
    ) -> Union[dict, None]:
        """
        Delete object from cache
        Args:
            key: str
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
            **kwargs - Extra data
        """
        key = self.__generate_key(
            key=key,
            channel=channel,
            user=user,
            content_object=content_object
        )
        # First check if object exists in cache or db
        get_cache = self.get_from_cache(
            key=key, channel=channel, user=user, content_object=content_object
        )
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
                pending_delete=True,
                content_object=content_object,
                **kwargs
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
            channel: Channel,
            content_object: models.Model = None,
    ) -> Union[dict, None]:
        """
        Search for an object in db
        Args:
            key: str
            user: settings.AUTH_USER_MODEL
            channel: Channel
            content_object: models.Model
        """
        cache_key = f'search_db_{key}'
        cached_object = cache.get(cache_key)

        if not cached_object:
            if content_object:
                # Check if object exists in db
                obj = self.model.objects.filter(
                    user=user,
                    channel=channel,
                    content_type=get_content_type_model(model=type(content_object)),
                    object_id=content_object.id
                )
            else:
                # Check if object exists in db
                obj = self.model.objects.filter(
                    user=user,
                    channel=channel
                )
            # Set object in cache and return it
            if obj.exists():
                return self.__set_cache(
                    key=cache_key,
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
        )
        return cache.get(key)

    def __get_all_from_cache(self, key: str) -> list:
        """
        Return all objects that are only saved in cache
        """
        cache_key = f"cache_{key}"
        cached_result = cache.get(cache_key)
        if cached_result is None:
            # Get all objects in cache
            caches = [
                cache.get(object_key) for object_key in cache.keys(key)
            ]

            # Filter objects that are only in cache, not saved in db
            cached_object = list(
                filter(
                    lambda obj: obj.get('source') == ObjectSource.CACHE.value,
                    caches
                )
            )
            cache.set(cache_key, cached_object, timeout=60)
            return cached_object

        return cached_result

    def __get_all_from_db(
            self, *,
            channel: Channel,
            **kwargs
    ) -> list:
        """
        Return all objects that are only saved in db (Based on args)
        """

        # Objects from db
        db_objects = list(
            self.model.objects.filter(channel=channel, **kwargs).values(
                'user', 'channel', 'date'
            )
        )
        return db_objects

    def __get_unique_objects(self, objects: list) -> list:
        """
        Remove duplicate users and check pending delete
        Args:
            objects: List of duplicated objects
        """
        unique_objects = []
        seen_users = set()

        for combined_object in objects:
            user = combined_object.get('user')
            # Check if user is new to the set
            if user not in seen_users:
                # Check object is not pending to delete later
                if combined_object.get('pending_delete') is not True:
                    unique_objects.append(combined_object)
                seen_users.add(user)

        return unique_objects

    def __generate_key(
            self,
            key: str,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            content_object: models.Model = None
    ) -> str:
        """
        Return a key based on the given key and args
        """
        user_token = user if user else '*'
        if content_object:
            return key.format(
                channel_token=channel.token,
                user_token=user_token,
                object_token=content_object.token
            )
        return key.format(channel_token=channel.token, user_token=user_token)
