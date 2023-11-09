from django.db.utils import IntegrityError
from django.core.cache import caches

import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestChannelSubscriber:
    def test_auto_create_sub_for_channel_owner(self, create_channel):
        """Ensure that a new channel automatically subscribes its owner."""
        assert create_channel.subscribers.count() == 1

    def test_raise_error_for_subscribing_twice(self, create_channel):
        """Ensure that users can only subscribe to a channel once."""
        with pytest.raises(IntegrityError):
            ChannelSubscriber.objects.create(
                user=create_channel.owner, channel=create_channel
            )

    def test_delete_subscriber(self, create_subscriber):
        assert create_subscriber.channel.subscribers.count() == 2
        create_subscriber.delete()
        assert create_subscriber.channel.subscribers.count() == 1

    def test_get_channel_subscriber_count(self, create_channel, create_superuser):
        assert ChannelSubscriber.objects.get_count(create_channel) == 1
        # Delete the old subscriber count in cache
        for cache_backend in caches.all():
            cache_backend.clear()
        ChannelSubscriber.objects.create(user=create_superuser, channel=create_channel)
        assert ChannelSubscriber.objects.get_count(create_channel) == 2
