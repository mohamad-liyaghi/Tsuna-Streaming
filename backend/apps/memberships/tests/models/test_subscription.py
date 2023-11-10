from memberships.models import Membership, Subscription
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
import pytest


@pytest.mark.django_db
class TestSubscriptionModel:
    def test_create_subscription_for_inactive_user_fails(
        self, inactive_user, membership
    ):
        assert not inactive_user.is_active
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(user=inactive_user, membership=membership)

    def test_create_subscription_for_superuser_fails(self, superuser, membership):
        assert superuser.is_superuser
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(user=superuser, membership=membership)

    def test_get_active_subscriptions(self, subscription):
        user = subscription.user
        assert Subscription.objects.get_active_subscription(user=user) == subscription

    def test_delete_subscription(self, subscription):
        user = subscription.user
        subscription.delete()
        user.refresh_from_db()
        assert user.is_normal()

    def test_subscription_is_active(self, subscription):
        assert subscription.is_active

    def test_subscribe_unavailable_plan(self, membership, user):
        membership.is_available = False
        membership.save()
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(user=user, membership=membership)

    def test_subscribe_twice_fails(self, subscription, membership):
        with pytest.raises(PermissionDenied):
            Subscription.objects.create(user=subscription.user, membership=membership)

    def test_get_active_sub_not_exist(self, inactive_user):
        assert not Subscription.objects.get_active_subscription(user=inactive_user)
