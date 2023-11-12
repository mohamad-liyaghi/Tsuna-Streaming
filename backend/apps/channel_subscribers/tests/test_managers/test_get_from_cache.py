import pytest
from channel_subscribers.models import ChannelSubscriber
from core.utils import ObjectSource
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestGetSubFromCache:
    def test_get_from_db(self, subscriber):
        sub = ChannelSubscriber.objects.get_from_cache(
            channel=subscriber.channel, user=subscriber.user
        )
        assert sub.get("source") == ObjectSource.DATABASE.value

    def test_get_cached(self, cached_subscriber, superuser, channel):
        sub = ChannelSubscriber.objects.get_from_cache(channel=channel, user=superuser)
        assert sub
