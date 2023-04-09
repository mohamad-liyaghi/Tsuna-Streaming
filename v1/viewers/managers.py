from django.db import models
from django.core.cache import cache

class ViewerManager(models.Manager):

    class ViewerManager(models.Manager):
        
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
                    }
                )
                return True

            # Return False if cache already exists
            return False
