import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestCreateInCache:
    def test_create_cached_subscriber(self, create_channel, create_superuser):
        ChannelSubscriber.objects.create_in_cache(
            channel=create_channel, user=create_superuser
        )
        assert ChannelSubscriber.objects.get_count(create_channel) == 2

    def test_create_cached_subscriber_twice(self, create_channel, create_superuser):
        ChannelSubscriber.objects.create_in_cache(
            channel=create_channel, user=create_superuser
        )
        # Second Time
        ChannelSubscriber.objects.create_in_cache(
            channel=create_channel, user=create_superuser
        )
        assert ChannelSubscriber.objects.get_count(create_channel) == 2
