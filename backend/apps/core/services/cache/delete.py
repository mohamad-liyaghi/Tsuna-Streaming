from django.core.cache import cache
from django.db import models
from django.conf import settings
from typing import Union
from channels.models import Channel
from core.utils import ObjectSource
from core.utils import get_content_type_model, generate_cache_key


class CacheDeleteMixin:
    """
    A mixin for deleting objects from cache and db
    """

    def delete_cache(
            self, *,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            content_object: models.Model = None,
            **kwargs
    ) -> Union[dict, None]:
        """
        Delete object from cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
            **kwargs - Extra data
        """
        key = generate_cache_key(
            key=self.raw_cache_key,
            channel=channel,
            user=user,
            content_object=content_object
        )

        # Check if object exists in db or cache
        get_cache = self.get_from_cache(
            channel=channel,
            user=user,
            content_object=content_object
        )

        # If not exists, Raise exception
        if not get_cache:
            raise ValueError("Object does not exist in cache or db.")

        # If object source is database, create a record so celery would delete it.
        if get_cache.get('source') != ObjectSource.CACHE.value:
            self._set_cache(
                key=key,
                channel=channel,
                user=user,
                pending_delete=True,
                content_object=content_object,
                **kwargs
            )
            return

        cache.delete(key)
        return
