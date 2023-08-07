from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.cache import cache
from typing import Union
from core.constants import CACHE_CONTENT_TYPE_KEY


def get_content_type_model(
        model: Union[models.Model, str] = "*",
        _id: Union[int, str] = "*",
) -> ContentType:
    """
    Get the content type for a model and return it.
    :param model: The model to get the content type for
    :param _id: The id of the content type
    """
    if model == '*' and _id == '*':
        raise ValueError("Either model or id must be provided")

    cached = cache.get_many(
        cache.keys(
            CACHE_CONTENT_TYPE_KEY.format(model=model, id=_id)
        )
    )

    if not cached:
        try:
            filters = {}

            if model != "*":
                filters['model'] = model.__name__.lower()

            if _id != "*":
                filters['id'] = _id

            content_type = ContentType.objects.get(**filters)

            # Set in cache if found
            cache.set(
                key=CACHE_CONTENT_TYPE_KEY.format(model=content_type, id=content_type.id),
                value={'id': content_type.id, 'model': content_type}
            )
            return content_type

        except ContentType.DoesNotExist:
            raise ValueError(f"Content type not found")

    return next(iter(cached.values()))['model']

