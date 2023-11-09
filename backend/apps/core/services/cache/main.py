from django.db import models
from .list import CacheListMixin
from .create import CacheCreateMixin
from .get import CacheGetMixin
from .delete import CacheDeleteMixin


class CacheService(CacheListMixin, CacheCreateMixin, CacheGetMixin, CacheDeleteMixin):
    """
    A service for handling cache operations.
    Methods (from parent classes):
        - create_cache()
        - get_from_cache()
        - get_list()
        - delete_cache()
    """

    def __init__(self, model: models.Model, cache_key: str):
        """
        Set the default model for the service
        """
        self.model = model
        self.raw_cache_key = cache_key
