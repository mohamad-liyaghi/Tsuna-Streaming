import pytest
from channel_subscribers.models import ChannelSubscriber
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestDeleteInCache:
    def test_delete_in_cache(self, create_cached_subscriber):
        channel = Channel.objects.get(id=create_cached_subscriber['channel'])

        ChannelSubscriber.objects.delete_in_cache(
            channel=channel,
            user=Account.objects.get(id=create_cached_subscriber['user'])
        )
        assert ChannelSubscriber.objects.get_count(channel=channel) == 1

    def test_delete_invalid_subscriber_in_cache(self, create_superuser, create_channel):
        with pytest.raises(ValueError):
            ChannelSubscriber.objects.delete_in_cache(
                user=create_superuser,
                channel=create_channel
            )

    def test_delete_subscriber_in_db(self, create_subscriber):
        assert ChannelSubscriber.objects.get_from_cache(
            channel=create_subscriber.channel,
            user=create_subscriber.user
        )
        ChannelSubscriber.objects.delete_in_cache(
            channel=create_subscriber.channel,
            user=create_subscriber.user
        )
        assert not ChannelSubscriber.objects.get_from_cache(
            channel=create_subscriber.channel,
            user=create_subscriber.user
        )
        assert ChannelSubscriber.objects.get_count(
            create_subscriber.channel
        ) == 1
