from django.conf import settings
from django.db import models
from typing import Optional, Union
from channels.models import Channel


def generate_cache_key(
    key: str,
    channel: Channel,
    user: Union[settings.AUTH_USER_MODEL, str] = "*",
    content_object: Optional[models.Model] = None,
) -> str:
    """
    Generate a cache key based on the given parameters.

    :param key: The base formattable string for the cache key.
    :param channel: The channel instance.
    :param user: The user instance or a string represent all (*).
    :param content_object: An optional content object instance.

    :return: The generated cache key.
    """

    # Use the user's token if available, otherwise use the user string
    user_token = user.token if hasattr(user, "token") else user

    if content_object:
        return key.format(
            channel_token=channel.token,
            user_token=user_token,
            object_token=content_object.token,
        )

    return key.format(channel_token=channel.token, user_token=user_token)
