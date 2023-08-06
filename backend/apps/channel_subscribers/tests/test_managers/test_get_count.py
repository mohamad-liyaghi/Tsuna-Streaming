import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestSubscriberCount:
    def test_get_count(self, create_subscriber):
        assert ChannelSubscriber.objects.get_count(create_subscriber.channel) == 2

    def test_get_count_sub_only_owner(self, create_channel):
        """
        By default the only subscriber is admin
        """
        assert ChannelSubscriber.objects.get_count(create_channel) == 1
