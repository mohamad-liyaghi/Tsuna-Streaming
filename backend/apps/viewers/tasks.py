from django.core.cache import cache
from celery import shared_task
from viewers.models import Viewer
from viewers.constants import CACHE_OBJECT_VIEWER
from core.utils import ObjectSource
from core.utils import get_content_type_model
from accounts.models import Account


@shared_task
def insert_viewer_into_db():
    """
    Insert Cached viewers to database.
    """

    # Get keys of all cached viewers
    viewer_keys = cache.keys(
        CACHE_OBJECT_VIEWER.format(
            channel_token='*', object_token='*', user_token='*'
        )
    )

    if viewer_keys:
        # Get all cached viewers
        all_viewers = cache.get_many(viewer_keys).values()

        # Filter those viewers that are cached
        cached_viewers = [
            viewer for viewer in all_viewers
            if viewer['source'] == ObjectSource.CACHE.value
        ]

        # Get all users of cached viewers
        users = Account.objects.filter(
            id__in=[viewer['user'] for viewer in cached_viewers]
        )

        # Create instances of Viewer model
        new_viewers = [
            Viewer(
                user=users.get(id=viewer['user']),
                content_object=viewer['content_object'],
                date=viewer['date'],
            ) for viewer in cached_viewers
        ]

        # Bulk Insert
        Viewer.objects.bulk_create(new_viewers)
        # Delete their cache
        cache.delete_many(viewer_keys)


@shared_task
def remove_object_viewers(content_type_id: int, object_id: int, object_token: str):
    """
    Remove viewers of an object after deleting it.
    """
    content_model = get_content_type_model(
        _id=content_type_id
    )

    # Delete all object viewers in db.
    Viewer.objects.filter(
        content_type=content_model,
        object_id=object_id
    ).delete()

    # Delete object viewers from cache
    cache.delete_pattern(
        CACHE_OBJECT_VIEWER.format(
            channel_token="*",
            object_token=object_token,
            user_token='*'
        )
    )
