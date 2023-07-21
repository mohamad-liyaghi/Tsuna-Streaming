import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestDeleteInCache:
    def test_delete_in_cache(self, create_cached_subscriber):
        ChannelSubscriber.objects.delete_in_cache(
            create_cached_subscriber['channel'],
            create_cached_subscriber['user']
        )
        assert ChannelSubscriber.objects.get_count(
            create_cached_subscriber['channel']
        ) == 1

    def test_delete_invalid_subscriber_in_cache(self):
        with pytest.raises(ValueError):
            ChannelSubscriber.objects.delete_in_cache(
                user='fake_user',
                channel='fake_channel'
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
        assert ChannelSubscriber.objects.get_count(
            create_subscriber.channel
        ) == 1
