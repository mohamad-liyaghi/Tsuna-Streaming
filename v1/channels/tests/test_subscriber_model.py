from accounts.models import Account
from channels.models import Channel, ChannelSubscriber
from django.db.utils import IntegrityError
import pytest

@pytest.mark.django_db
class TestChannelModel:
    
    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="channel")
    
    def test_auto_create_sub_for_channel_owner(self):
        assert (self.channel.subscribers.count(), 1)

    def test_raise_error_for_susbcibing_twice(self):
        '''Users can only subscribe a channel once'''
        with pytest.raises(IntegrityError):
            ChannelSubscriber.objects.create(user=self.user, channel=self.channel)


    