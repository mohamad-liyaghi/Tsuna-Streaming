from core.managers import BaseCacheManager
from votes.services import VoteService
from votes.constants import CACHE_OBJECT_VOTE


class VoteManager(BaseCacheManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = None
        self.cache_key = None

    def contribute_to_class(self, model, name):
        super().contribute_to_class(model, name)
        self.service = VoteService(self.model)
        self.cache_key = CACHE_OBJECT_VOTE

