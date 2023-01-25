from accounts.models import Account
from channels.models import Channel, ChannelSubscriber
import pytest

@pytest.mark.django_db
class TestChannelModel:
    
    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="channel")
    
    def test_auto_create_sub_for_channel_owner(self):
        assert (self.channel.subscribers.count(), 1)


    