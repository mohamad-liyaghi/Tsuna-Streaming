import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
def test_create_subscriber(create_subscriber):
    assert create_subscriber.channel.subscribers.count() == 2


@pytest.mark.django_db
def test_create_cached_subscriber(create_cached_subscriber):
    assert ChannelSubscriber.objects.get_count(
        create_cached_subscriber['channel']
    ) == 2
