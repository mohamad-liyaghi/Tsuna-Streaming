from django.db.utils import IntegrityError
from django.core.cache import caches

import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestChannelSubscriber:
    def test_auto_create_sub_for_channel_owner(self, channel):
        """Ensure that a new channel automatically subscribes its owner."""
        assert channel.subscribers.count() == 1

    def test_raise_error_for_subscribing_twice(self, channel):
        """Ensure that users can only subscribe to a channel once."""
        with pytest.raises(IntegrityError):
            ChannelSubscriber.objects.create(user=channel.owner, channel=channel)

    def test_delete_subscriber(self, subscriber):
        assert subscriber.channel.subscribers.count() == 2
        subscriber.delete()
        assert subscriber.channel.subscribers.count() == 1

    def test_get_channel_subscriber_count(self, channel, superuser):
        assert (
            ChannelSubscriber.objects.get_count(channel) == 2
        )  # One in cache + one in db
        ChannelSubscriber.objects.all().delete()
        # Delete the old subscriber count in cache
        for cache_backend in caches.all():
            cache_backend.clear()
        ChannelSubscriber.objects.create(user=superuser, channel=channel)
        assert ChannelSubscriber.objects.get_count(channel) == 1
