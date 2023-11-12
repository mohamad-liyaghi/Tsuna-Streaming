import pytest
from channel_subscribers.models import ChannelSubscriber
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestDeleteInCache:
    def test_delete_in_cache(self, cached_subscriber):
        channel = Channel.objects.get(id=cached_subscriber["channel"])

        ChannelSubscriber.objects.delete_in_cache(
            channel=channel,
            user=Account.objects.get(id=cached_subscriber["user"]),
        )
        assert ChannelSubscriber.objects.get_count(channel=channel) == 1

    def test_delete_invalid_subscriber_in_cache(self, superuser, channel):
        with pytest.raises(ValueError):
            ChannelSubscriber.objects.delete_in_cache(user=superuser, channel=channel)

    def test_delete_subscriber_in_db(self, subscriber):
        assert ChannelSubscriber.objects.get_from_cache(
            channel=subscriber.channel, user=subscriber.user
        )
        ChannelSubscriber.objects.delete_in_cache(
            channel=subscriber.channel, user=subscriber.user
        )
        assert not ChannelSubscriber.objects.get_from_cache(
            channel=subscriber.channel, user=subscriber.user
        )
        assert ChannelSubscriber.objects.get_count(subscriber.channel) == 1
