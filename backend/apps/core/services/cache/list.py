from django.core.cache import cache
from django.db import models
from django.db.models import Value
from typing import Optional
from channels.models import Channel
from core.utils import ObjectSource
from core.utils import get_content_type_model, generate_cache_key


class CacheListMixin:
    """
    This mixin is used for retrieving list of objects from cache and db.
    """

    def get_list(
            self,
            channel: Channel,
            content_object: Optional[models.Model] = None,
            **kwargs
    ) -> list:
        """
        Return list of objects from both cache and db (without duplication).
        Args:
            channel: Channel object
            content_object: Content object
            **kwargs: Additional arguments
        """

        # Set content_object in kwargs for passing to _get_list_from_db
        if content_object is not None:
            kwargs.setdefault('content_object', content_object)

        key = generate_cache_key(
            key=self.raw_cache_key,
            channel=channel,
            content_object=content_object
        )

        cache_list = self._get_list_from_cache(key=key)
        database_list = self._get_list_from_db(
            key=key,
            channel=channel,
            **kwargs
        )

        unique_objects = self._remove_duplication(
            objects=cache_list + database_list
        )

        return unique_objects

    def _get_list_from_db(
            self,
            key: str,
            channel: Channel,
            **kwargs
    ) -> list:
        """
        Return List of objects from db
        Args:
            key: Cache key
            channel: Channel object
            **kwargs: Additional arguments
        """

        if content_object := kwargs.pop('content_object', None):
            content_model = get_content_type_model(
                model=type(content_object)
            )
            # Set content_type and object_id in kwargs
            kwargs.setdefault('content_type', content_model)
            kwargs.setdefault('object_id', content_object.id)

        database_objects = list(
            self.model.objects.filter(
                channel=channel, **kwargs
            ).values(
                'user', 'channel', 'date'
            ).annotate(
                source=Value(ObjectSource.DATABASE.value)
            )
        )
        return database_objects

    def _get_list_from_cache(self, key: str) -> list:
        """
        Return List of objects from cache
        Args:
            key: Cache key
        """
        caches = [
            cache.get(object_key) for object_key in cache.keys(key)
        ]

        # Filter those objects which are from cache
        filtered_result = list(filter(
            lambda obj: obj.get('source') == ObjectSource.CACHE.value
            if isinstance(obj, dict) else False,
            caches
        ))

        return filtered_result

    @staticmethod
    def _remove_duplication(objects: list) -> list:
        """
        Return distinct objects
        Args:
            objects: List of objects
        """
        unique_objects = []
        seen_users = set()

        for combined_object in objects:
            user = combined_object.get('user')
            # Check if user is new to the set
            if user not in seen_users:
                # Check object is not pending to delete later
                if not combined_object.get('pending_delete'):
                    unique_objects.append(combined_object)
                seen_users.add(user)

        return unique_objects
