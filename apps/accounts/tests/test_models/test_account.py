import pytest
from accounts.models import Account, Token


@pytest.mark.django_db
class TestAccountModel:

    def setup(self):
        """Create simple and super user"""
        self.simple_user = Account.objects.create_user(
            email="simple@simple.com",
            password="1234USERnormal"
        )
        self.super_user = Account.objects.create_superuser(
            email="superuser@superuser.com",
            password="1234USERnormal"
        )
    
    def test_simple_user_is_not_active(self):
        """Simple users are not active until they verify their email."""

        assert not self.simple_user.is_active
        # token gets created after a users add to db
        assert Token.objects.filter(user=self.simple_user).exists()
    
    def test_superuser_is_active(self):
        """Super users are active by default."""
        assert self.super_user.is_active

    def test_user_token(self):
        """User token from AbstractTokenModel"""
        assert self.simple_user.token is not None
        assert self.super_user.token is not None

    def test_user_full_name(self, create_active_user):
        """User full name from AbstractUserModel"""
        assert (
                create_active_user.full_name ==
                create_active_user.first_name + " " + create_active_user.last_name
        )
