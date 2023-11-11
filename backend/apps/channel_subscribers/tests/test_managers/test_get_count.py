import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestSubscriberCount:
    def test_get_count_sub_only_owner(self, channel):
        assert ChannelSubscriber.objects.get_count(channel) == 1

    def test_get_count(self, subscriber):
        assert ChannelSubscriber.objects.get_count(subscriber.channel) == 2
