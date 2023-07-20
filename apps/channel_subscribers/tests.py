from django.db.utils import IntegrityError
from django.core.cache import cache, caches

import pytest

from accounts.models import Account
from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestChannelSubscriber:
    def setup_method(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.user.is_active = True
        self.user.save()
        self.subscriber_user = Account.objects.create_user(email="sub@sub.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="channel")

    def create_subscriber(self):
        self.subscriber = ChannelSubscriber.objects.subscribe_in_cache(self.channel.token, self.subscriber_user.token)

    def test_auto_create_sub_for_channel_owner(self):
        """Ensure that a new channel automatically subscribes its owner."""
        assert self.channel.subscribers.count() == 1

    def test_raise_error_for_subscribing_twice(self):
        """Ensure that users can only subscribe to a channel once."""
        with pytest.raises(IntegrityError):
            ChannelSubscriber.objects.create(user=self.user, channel=self.channel)

    def test_create_subscriber(self):
        """Ensure that a subscriber is created and cached."""
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}') is None
        self.create_subscriber()
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}') is not None

    def test_get_subscriber(self):
        """Ensure that a subscriber can be retrieved from the cache."""
        assert ChannelSubscriber.objects.get_from_cache(self.channel.token, self.subscriber_user.token) is None
        self.create_subscriber()
        assert ChannelSubscriber.objects.get_from_cache(self.channel.token, self.subscriber_user.token) is not None

    def test_delete_subscriber(self):
        """Ensure that a subscriber can be deleted and marked as unsubscribed."""
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}') is None
        self.create_subscriber()
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}') is not None    
        ChannelSubscriber.objects.unsubscribe_in_cache(self.channel.token, self.subscriber_user.token)
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}')['subscription_status'] == 'unsubscribed'

    def test_get_channel_subscriber_count(self):
        assert ChannelSubscriber.objects.get_count(self.channel) == 1
        # Delete the old subscriber count in cache
        for cache_backend in caches.all():
            cache_backend.clear()
        self.create_subscriber()
        assert ChannelSubscriber.objects.get_count(self.channel) == 2
