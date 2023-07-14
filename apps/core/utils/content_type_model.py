from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.cache import cache
from typing import Union


def get_content_type_model(
        model: models.Model,
        return_id: bool = False
) -> Union[models.Model, int, None]:
    """
    Get the content type model for the given model
    :param model: The model to get the content type for
    :param return_id: Whether to return the id or the model
    """
    cached = cache.get(f'content_type:{model}')

    # If not set in cache
    if cached is None:
        # Get content type for the model
        content_type = ContentType.objects.get_for_model(model)

        if content_type:
            # Set in cache if found
            cache.set(
                key=f'content_type:{model}',
                value={'id': content_type.id, 'model': content_type}
            )

            # Get from cache
            cached = cache.get(f'content_type:{model}')
            # Return id if requested
            if return_id:
                return cached['id']
            # Otherwise return model
            return cached['model']

        # Return None if not found
        return

    # Return id if requested
    if return_id:
        return cached['id']

    # Otherwise return model
    return cached['model']
