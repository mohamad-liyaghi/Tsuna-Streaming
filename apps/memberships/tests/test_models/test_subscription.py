from memberships.models import Membership, Subscription
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
import pytest


@pytest.mark.django_db
class TestSubscriptionModel:

    @pytest.fixture(autouse=True)
    def setup(self, create_active_user):
        # TODO: make a fixture for this
        self.user = create_active_user
        self.membership = Membership.objects.create(title="membership", active_months=1)

    def test_create_subscription(self):
        Subscription.objects.create(
            user=self.user,
            membership=self.membership
        )
        self.user.refresh_from_db()
        assert self.user.is_premium()

    def test_create_subscription_for_deactive_user(self, create_deactive_user):
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(
                user=create_deactive_user,
                membership=self.membership
            )

    def test_create_subscription_for_superuser(self, create_superuser):
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(
                user=create_superuser,
                membership=self.membership
            )

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(
            user=self.user,
            membership=self.membership
        )
        subscription.delete()
        self.user.refresh_from_db()
        assert self.user.is_normal()

    def test_subscription_is_active(self):
        subscription = Subscription.objects.create(
            user=self.user,
            membership=self.membership
        )
        assert subscription.is_active

    def test_subscription_is_not_active(self):
        subscription = Subscription.objects.create(
            user=self.user,
            membership=self.membership
        )
        subscription.end_date = timezone.now() - datetime.timedelta(days=1)
        subscription.save()
        assert not subscription.is_active

# TODO: get active subs