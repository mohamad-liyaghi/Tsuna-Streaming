import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestGetSubFromCache:
    def test_get_cached(self, create_cached_subscriber):
        sub = ChannelSubscriber.objects.get_from_cache(
            channel=create_cached_subscriber['channel'],
            user=create_cached_subscriber['user']
        )
        assert sub['source'] == 'cache'

    def test_get_from_db(self, create_subscriber):
        sub = ChannelSubscriber.objects.get_from_cache(
            channel=create_subscriber.channel,
            user=create_subscriber.user
        )
        assert sub['source'] == 'database'
