from django.db.utils import IntegrityError
from django.core.cache import cache

import pytest

from accounts.models import Account
from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestChannelSubscriber:
    def setup_method(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.subscriber_user = Account.objects.create_user(email="sub@sub.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="channel")

    def create_subscriber(self):
        self.subscriber = ChannelSubscriber.create_subscriber(self.channel.token, self.subscriber_user.token)

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
        assert ChannelSubscriber.get_subscriber(self.channel.token, self.subscriber_user.token) is None
        self.create_subscriber()
        assert ChannelSubscriber.get_subscriber(self.channel.token, self.subscriber_user.token) is not None

    def test_delete_subscriber(self):
        """Ensure that a subscriber can be deleted and marked as unsubscribed."""
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}') is None
        self.create_subscriber()
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}') is not None    
        ChannelSubscriber.delete_subscriber(self.channel.token, self.subscriber_user.token)
        assert cache.get(f'subscriber:{self.channel.token}:{self.subscriber_user.token}')['subscription_status'] == 'unsubscribed'

    def test_get_channel_subscriber_count(self):
        """Ensure that the number of subscribers for a channel can be retrieved from the cache and DB."""
        assert self.channel.subscribers_count == 1
        # Delete the old subscriber count in cache
        cache.delete(f'subscriber_count:{self.channel.token}')
        self.create_subscriber()
        assert self.channel.subscribers_count == 2
