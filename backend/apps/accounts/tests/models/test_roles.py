import pytest


@pytest.mark.django_db
class TestAccountRole:
    def test_superuser_is_admin(self, superuser):
        assert superuser.is_admin()

    def test_active_user_is_normal(self, user):
        assert user.is_normal()

    def test_user_with_subscription_is_premium(self, create_subscription):
        assert create_subscription.user.is_premium()
