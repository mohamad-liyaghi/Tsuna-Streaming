from core.managers import BaseCacheManager
from viewers.services import ViewerService
from viewers.constants import CACHE_OBJECT_VIEWER


class ViewerManager(BaseCacheManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = None
        self.cache_key = None

    def contribute_to_class(self, model, name):
        super().contribute_to_class(model, name)
        self.service = ViewerService(self.model)
        self.cache_key = CACHE_OBJECT_VIEWER

    def delete_in_cache(self):
        """Make delete viewer unavailable in cache."""
        pass
