import pytest
from memberships.models import Membership, Subscription


@pytest.mark.django_db
def test_create_membership(create_membership):
    assert Membership.objects.count() == 1


@pytest.mark.django_db
def test_create_subscription(create_subscription):
    assert Subscription.objects.count() == 1


@pytest.mark.django_db
def test_subscriptions_plan(create_membership, create_subscription):
    assert create_subscription.membership == create_membership
