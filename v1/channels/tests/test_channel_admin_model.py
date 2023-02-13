from accounts.models import Account
from channels.models import Channel, ChannelAdmin, ChannelSubscriber
from django.core.exceptions import ValidationError
import pytest

@pytest.mark.django_db
class TestChannelAdminModel:

    def create_admin(self):
        self.admin = ChannelAdmin.objects.create(user=self.simple_user, channel=self.channel, promoted_by=self.super_user)

    def create_subscriber(self):
        self.subscriber = ChannelSubscriber.objects.create(channel=self.channel, user=self.simple_user)

    
    def setup(self):
        self.simple_user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.super_user = Account.objects.create_superuser(email="superuser@superuser.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.super_user, title="test")    

    
    def test_raise_error_when_user_hasnt_subscribed(self):
        '''While user hasnt subscribed to channel, use cannot be promoted'''
        assert self.simple_user.channel_admin.count() == 0
        with pytest.raises(ValidationError):
            self.create_admin()


    def test_add_admin(self):
        assert self.simple_user.channel_admin.count() == 0
        # create a subscriber instance
        self.create_subscriber()
        # create an admin
        self.create_admin()
        assert self.simple_user.channel_admin.count() == 1


    def test_raise_error_when_duplicating_admin(self):
        '''user cannot be promoted for 2 times'''
        assert self.simple_user.channel_admin.count() == 0
        # create a subscriber instance
        self.create_subscriber()
        # create an admin
        self.create_admin()
        assert self.simple_user.channel_admin.count() == 1

        with pytest.raises(ValueError):
            self.create_admin()
    
    def test_delete_admin_after_unsubscribing(self):
        '''When a user unsubscribe a channel, the admin instance will be deleted.'''
        
        self.create_subscriber()
        self.create_admin()
        assert self.channel.admins.count() == 1
        self.subscriber.delete()
        assert self.channel.admins.count() == 0