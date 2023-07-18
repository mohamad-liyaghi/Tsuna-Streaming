from accounts.models import Account
from memberships.models import Membership, Subscription
from memberships.exceptions import MembershipInUserError
from django.utils import timezone
import datetime
import pytest


@pytest.mark.django_db
class TestMembershipModel:

    @pytest.fixture(autouse=True)
    def setup(self, create_active_user):
        # TODO: make a fixture for this
        self.user = create_active_user
        self.membership = Membership.objects.create(title="membership", active_months=1)

    def test_create_membership(self):
        membership = Membership.objects.create(
            title="Test membership", active_months=1
        )
        assert membership.title == "Test membership"

    def test_delete(self):
        self.membership.delete()
        assert Membership.objects.count() == 0

    def test_delete_with_subscription(self):
        Subscription.objects.create(
            user=self.user,
            membership=self.membership
        )
        with pytest.raises(MembershipInUserError):
            self.membership.delete()
