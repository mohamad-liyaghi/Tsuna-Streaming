import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.fixture
def create_subscriber(channel, superuser):
    return ChannelSubscriber.objects.create(user=superuser, channel=channel)


@pytest.fixture
def create_cached_subscriber(create_channel, create_superuser):
    return ChannelSubscriber.objects.create_in_cache(
        channel=create_channel, user=create_superuser
    )
