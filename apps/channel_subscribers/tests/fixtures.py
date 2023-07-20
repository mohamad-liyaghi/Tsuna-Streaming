import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.fixture
def create_subscriber(create_channel, create_superuser):
    return ChannelSubscriber.objects.create(
        user=create_superuser,
        channel=create_channel
    )
