import pytest


@pytest.mark.django_db
class TestAccountRole:

    def test_is_admin(self, create_superuser):
        assert create_superuser.is_admin()

    # TODO: make this work with fixtures
    # def test_is_premium(self, create_account):
    #     assert not account.is_premium()

    def test_is_normal(self, create_active_user):
        assert create_active_user.is_normal()
