import pytest
from channel_subscribers.models import ChannelSubscriber
from core.utils import ObjectSource
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestGetSubFromCache:
    def test_get_cached(self, create_cached_subscriber):
        sub = ChannelSubscriber.objects.get_from_cache(
            channel=Channel.objects.get(id=create_cached_subscriber["channel"]),
            user=Account.objects.get(id=create_cached_subscriber["user"]),
        )
        assert sub["source"] == "cache"

    def test_get_from_db(self, create_subscriber):
        sub = ChannelSubscriber.objects.get_from_cache(
            channel=create_subscriber.channel, user=create_subscriber.user
        )
        assert sub.get("source") == ObjectSource.DATABASE.value
