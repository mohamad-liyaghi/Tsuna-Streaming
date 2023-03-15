import pytest
from accounts.models import Account
from channels.models import Channel, ChannelSubscriber
from channel_admins.models import ChannelAdmin 
from django.core.exceptions import PermissionDenied
from channel_admins.exceptions import DuplicatePromotionException, SubscriptionRequiredException


@pytest.mark.django_db
class TestAdminModel:

    def create_admin(self):
        self.admin = ChannelAdmin.objects.create(user=self.simple_user, channel=self.channel, promoted_by=self.super_user)

    def create_subscriber(self):
        self.subscriber = ChannelSubscriber.objects.create(channel=self.channel, user=self.simple_user)

    
    def setup(self):
        self.simple_user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.super_user = Account.objects.create_superuser(email="superuser@superuser.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.super_user, title="test")    

    def test_create_admin_after_creating_channel(self):
        assert self.super_user.admin.count() == 1

    def test_add_admin(self):

        assert self.simple_user.admin.count() == 0

        # create a subscriber instance
        self.create_subscriber()
        # create an admin
        self.create_admin()

        assert self.simple_user.admin.count() == 1
    
    def test_delete_admin_after_unsubscribing(self):
        '''When a user unsubscribe a channel, the admin instance will be deleted.'''
        
        self.create_subscriber()
        self.create_admin()

        assert self.channel.admins.count() == 2
        self.subscriber.delete()
        assert self.channel.admins.count() == 1

    
    def test_create_permission(self):
        '''A signal for creating Permission object after creating an Admin object.'''
        self.create_subscriber()
        self.create_admin()

        assert self.admin.permissions.count() != 0

    def test_default_admin_permission_for_normal_user(self):
        '''By default Channel admins do not have any permission'''
        self.create_subscriber()
        self.create_admin()

        assert self.admin.permissions.first().add_object == False

    
    def test_default_admin_permission_for_super_user(self):
        '''By default Chanenl owner has all the permissions'''

        admin = self.super_user.admin.first().permissions.first()
        assert admin.add_object == True

    def test_raise_permission_denied_for_promoting(self):
        '''Users that dont have permission to add admin, gets PermissionDenied'''

        self.create_subscriber()
        with pytest.raises(PermissionDenied):
            ChannelAdmin.objects.create(user=self.simple_user, channel=self.channel, promoted_by=self.simple_user)

    def test_raise_error_promoting_unsubscribed_user(self):
        '''While user hasnt subscribed to channel, use cannot be promoted'''

        assert self.simple_user.admin.count() == 0

        with pytest.raises(SubscriptionRequiredException):
            self.create_admin()

    def test_raise_error_when_duplicating_admin(self):
        '''user cannot be promoted for 2 times'''

        assert self.simple_user.admin.count() == 0
        # create a subscriber instance
        self.create_subscriber()
        # create an admin
        self.create_admin()
        assert self.simple_user.admin.count() == 1

        with pytest.raises(DuplicatePromotionException):
            self.create_admin()