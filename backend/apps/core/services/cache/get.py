from django.db import models
from django.conf import settings
from typing import Optional, Union
from channels.models import Channel


class CacheGetMixin:
    """
    A mixin for retrieving objects from cache and db
    """

    def get_from_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            content_object: Optional[models.Model] = None,
    ) -> Union[dict, None]:
        """
        Retrieve an object from cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
        """
        return self._get_cache(
            channel=channel,
            user=user,
            content_object=content_object
        )

    def _get_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            content_object: Optional[models.Model] = None,
    ):
        """
        Filter and return an object from list.
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            content_object: models.Model
        """

        # Get list of objects
        object_list = self.get_list(
            channel=channel,
            content_object=content_object
        )

        if object_list:
            # Filter by user
            filtered_result = next(
                filter(
                    lambda dictionary: dictionary.get('user', None) == user.id,
                    object_list
                ),
                None
            )
            if filtered_result and not filtered_result.get('pending_delete', False):
                return filtered_result

        return
