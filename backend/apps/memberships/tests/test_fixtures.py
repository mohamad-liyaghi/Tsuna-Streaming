import pytest
from memberships.models import Membership, Subscription


@pytest.mark.django_db
def test_membership_is_created(membership):
    assert Membership.objects.filter(title=membership.title).exists()


@pytest.mark.django_db
def test_subscription_is_created(subscription):
    assert Subscription.objects.filter(user=subscription.user).exists()


@pytest.mark.django_db
def test_subscriptions_plan(membership, subscription):
    assert subscription.membership == membership


@pytest.mark.django_db
def test_create_premium_user(premium_user):
    assert premium_user.is_premium()
