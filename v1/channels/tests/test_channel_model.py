from accounts.models import Account
from channels.models import Channel
from memberships.models import Subscription, Membership
from channels.exceptions import ChannelLimitExceededException
import pytest

@pytest.mark.django_db
class TestChannelModel:
    
    def setup(self):
        self.simple_user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.super_user = Account.objects.create_superuser(email="superuser@superuser.com", password="1234USERnormal")


    def create_premium_user(self):    
        self.premium_user = Account.objects.create_user(email="user1@simple.com", password="1234USERnormal")
        membership = Membership.objects.create(title="plan", active_months=1)
        Subscription.objects.create(user=self.premium_user, membership=membership)


    def test_create_channel(self):
        '''Simply create a channel'''
        Channel.objects.create(owner=self.super_user, title="test")
        assert self.super_user.channels.count() == 1


    def test_channel_limit_for_superuser(self):
        '''Superuser can create unlimited channels.'''

        for _ in range(1, 12):
            Channel.objects.create(owner=self.super_user, title="test")

        assert self.super_user.channels.count() == 11


    def test_channel_limit_for_normal_user(self):
        '''Normal users can create less than 5 channels.'''
        
        for _ in range(1, 5):
            Channel.objects.create(owner=self.simple_user, title="test")

        assert self.simple_user.channels.count() == 4
        Channel.objects.create(owner=self.simple_user, title="test")
        assert self.simple_user.channels.count() == 5

        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=self.simple_user, title="test")

    def test_channel_limit_for_premium_user(self):
        '''Premium users can create 10 channels.'''

        self.create_premium_user()

        for _ in range(1, 11):
            Channel.objects.create(owner=self.premium_user, title="test")

        assert self.premium_user.channels.count() == 10

        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=self.premium_user, title="test")


    def test_channel_limit_for_former_premium_user(self):
        '''Old premium users that has created more than 5 channels can create channels up to 10.'''

        self.create_premium_user()

        for _ in range(1, 11):
            Channel.objects.create(owner=self.premium_user, title="test")
        
        assert self.premium_user.channels.count() == 10

        self.premium_user.role = 'n'
        self.premium_user.save()

        assert self.premium_user.channels.count() == 10 

        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=self.premium_user, title="test")