from accounts.models import Account
from memberships.models import Membership, Subscription
from memberships.exceptions import MembershipInUserError
import pytest


@pytest.mark.django_db
class TestMembershipModel:
    def test_create_membership(self):
        membership = Membership.objects.create(
            title="Test membership", active_months=1, is_available=True
        )
        assert membership.title == "Test membership"

    def test_delete(self, create_membership):
        create_membership.delete()
        assert Membership.objects.count() == 0

    def test_delete_with_subscription(self, create_membership, create_subscription):
        assert create_membership.subscriptions.count() == 1
        with pytest.raises(MembershipInUserError):
            create_membership.delete()
