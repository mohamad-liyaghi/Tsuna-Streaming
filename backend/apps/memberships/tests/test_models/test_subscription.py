from memberships.models import Membership, Subscription
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
import pytest


@pytest.mark.django_db
class TestSubscriptionModel:
    def test_create_subscription(self, create_active_user, create_membership):
        Subscription.objects.create(
            user=create_active_user,
            membership=create_membership,
        )
        create_active_user.refresh_from_db()
        assert create_active_user.is_premium()

    def test_create_subscription_for_deactive_user(
        self, create_deactive_user, create_membership
    ):
        assert not create_deactive_user.is_active
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(
                user=create_deactive_user, membership=create_membership
            )

    def test_create_subscription_for_superuser(
        self, create_superuser, create_membership
    ):
        assert create_superuser.is_superuser
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(
                user=create_superuser, membership=create_membership
            )

    def test_delete_subscription(self, create_subscription):
        user = create_subscription.user
        create_subscription.delete()
        user.refresh_from_db()
        assert user.is_normal()

    def test_subscription_is_active(self, create_subscription):
        assert create_subscription.is_active

    def test_subscription_is_not_active(self, create_subscription):
        create_subscription.end_date = timezone.now() - datetime.timedelta(days=1)
        create_subscription.save()
        assert not create_subscription.is_active

    def test_subscrive_unavailable_plan(self, create_membership, create_active_user):
        create_membership.is_available = False
        create_membership.save()
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(
                user=create_active_user, membership=create_membership
            )

    def test_subscribe_twice(self, create_subscription, create_membership):
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(
                user=create_subscription.user, membership=create_membership
            )

    def test_get_active_subscriptions(self, create_subscription):
        user = create_subscription.user
        assert (
            Subscription.objects.get_active_subscription(user=user)
            == create_subscription
        )

    def test_get_active_sub_not_exist(self, create_active_user):
        assert not Subscription.objects.get_active_subscription(user=create_active_user)
