import pytest
from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
def test_create_subscriber(subscriber):
    assert subscriber.channel.subscribers.count() == 2


@pytest.mark.django_db
def test_create_cached_subscriber(cached_subscriber):
    assert (
        ChannelSubscriber.objects.get_count(
            channel=Channel.objects.get(id=cached_subscriber["channel"])
        )
        == 2
    )
