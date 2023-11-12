import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestCreateInCache:
    def test_create_cached_subscriber(self, channel, superuser):
        ChannelSubscriber.objects.create_in_cache(channel=channel, user=superuser)
        assert ChannelSubscriber.objects.get_count(channel) == 2

    def test_create_cached_subscriber_twice(self, channel, superuser):
        ChannelSubscriber.objects.create_in_cache(channel=channel, user=superuser)
        # Second Time
        ChannelSubscriber.objects.create_in_cache(channel=channel, user=superuser)
        assert ChannelSubscriber.objects.get_count(channel) == 2
