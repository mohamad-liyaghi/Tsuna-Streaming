from accounts.models import Account
from channels.models import Channel
import pytest

@pytest.mark.django_db
class TestChannelModel:
    
    def setup(self):
        self.simple_user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.super_user = Account.objects.create_superuser(email="superuser@superuser.com", password="1234USERnormal")

    
    def test_create_channel(self):
        '''Simply create a channel'''
        Channel.objects.create(owner=self.super_user, title="test")
        assert self.super_user.channels.count() == 1

    def test_channel_limit(self):
        '''Premium/Admin users can create less than 10 channels'''

        # create 10 channels, After this user is not able to create the 11th channel
        with pytest.raises(ValueError):
            for _ in range(1, 12):
                Channel.objects.create(owner=self.super_user, title="test")    

        assert self.super_user.channels.count() == 10

    


        