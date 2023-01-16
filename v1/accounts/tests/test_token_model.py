from accounts.models import Token, Account
import pytest

@pytest.mark.django_db
class TestTokenModel:
    
    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.token = Token.objects.create(user=self.user)
    
    def test_token_create_after_creating_user(self):
        assert Token.objects.count() == 2 # one creates after creating user and one created in setup method
    
    def test_check_token_is_valid(self):
        assert self.token.is_valid == True
    
    def test_check_token_gets_deleted_after_deleting_user(self):
        self.user.delete()
        assert Token.objects.count() == 0
    
        
    
    


        