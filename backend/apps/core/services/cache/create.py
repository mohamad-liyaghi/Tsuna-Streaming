from django.core.cache import cache
from django.db import models
from django.conf import settings
from channels.models import Channel
from typing import Optional, Union
from datetime import datetime
from core.utils import ObjectSource
from core.utils import get_content_type_model, generate_cache_key


class CacheCreateMixin:
    """
    A mixin for creating object in cache and db
    """

    def create_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            content_object: Optional[models.Model] = None,
            **kwargs
    ) -> Union[dict, None]:
        """
        Create a new object in cache (if not exist)
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
            **kwargs: dict - Extra data
        """
        key = generate_cache_key(
            key=self.raw_cache_key,
            channel=channel,
            user=user,
            content_object=content_object
        )

        # Ensure that the object is not already in cache
        if self.get_from_cache(
                channel=channel,
                user=user,
                content_object=content_object
        ):
            return

        # If not exist, create a new object in cache
        return self._set_cache(
            key=key,
            channel=channel,
            user=user,
            content_object=content_object,
            **kwargs
        )

    def _set_cache(
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
