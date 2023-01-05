from accounts.models import Account
import pytest

@pytest.mark.django_db
class TestAccountModel:
    
    def setup(self):
        self.simple_user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.super_user = Account.objects.create_superuser(email="superuser@superuser.com", password="1234USERnormal")
    
    def test_simple_user_is_not_active(self):
        '''Simple users by default are not active. they must verify their accounts via email.'''
        assert self.simple_user.is_active == False
    
    def test_superuser_is_active(self):
        '''Superusers are active even without verification.'''
        assert self.super_user.is_active == True
    


        