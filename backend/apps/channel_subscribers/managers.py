from core.managers import BaseCacheManager
from channel_subscribers.services import ChannelSubscriberService
from channel_subscribers.constants import CACHE_SUBSCRIBER_KEY


class ChannelSubscriberManager(BaseCacheManager):
    """
    A manager for subscriber model which uses Subscriber Service for
    CRUD operations in cache
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = None
        self.cache_key = None

    def contribute_to_class(self, model, name):
        super().contribute_to_class(model, name)
        self.service = ChannelSubscriberService(self.model)
        self.cache_key = CACHE_SUBSCRIBER_KEY

