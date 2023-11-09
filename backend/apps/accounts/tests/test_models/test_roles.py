import pytest


@pytest.mark.django_db
class TestAccountRole:
    def test_is_admin(self, create_superuser):
        assert create_superuser.is_admin()

    def test_is_premium(self, create_subscription):
        assert create_subscription.user.is_premium()

    def test_is_normal(self, create_active_user):
        assert create_active_user.is_normal()
