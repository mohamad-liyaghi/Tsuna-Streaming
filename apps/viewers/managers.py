from django.db import models
from django.core.cache import cache
from django.utils import timezone

class ViewerManager(models.Manager):

    def get_from_cache(self, obj, user):
        """Check if viewer exists for an object in db/cache or not"""

        # get viewer from cache
        key = f'viewer:{obj.token}:{user.token}'
        cached_viewer = cache.get(key)
        
        # Return viewer if exist in cache
        if cached_viewer is not None:
            return cached_viewer
        
        # Return viewer and set it in cache, if viewer exists in db
        elif (viewer:=obj.viewers.filter(user=user).first()):
            cache.set(
                key=key,
                value={
                    'source': 'database',
                    'date' : viewer.date
                }
            )
            return cache.get(key)
        
        # return None if viewer does not exist
        return None


    def create_in_cache(self, object_token: str, user_token: str) -> bool:
        """
        Create a new viewer object in the cache.

        Args:
            object_token (str): The token of the object being viewed.
            user_token (str): The token of the user viewing the object.

        Returns:
            bool: True if viewer was created in cache, False otherwise.
        """

        # Check if viewer already exists in cache
        key = f'viewer:{object_token}:{user_token}'
        cached_viewer = cache.get(key)

        if not cached_viewer:
            # Create a cache record if it doesn't exist
            cache.set(
                key=key,
                value={
                    'source': 'cache',
                    'date' : timezone.now(),
                }
            )
            return True

        # Return False if cache already exists
        return False


# TODO: add get_viewer_count