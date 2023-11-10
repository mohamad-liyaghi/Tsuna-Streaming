import pytest
from memberships.models import Membership, Subscription


@pytest.fixture
def create_membership():
    """
    Simply create a membership
    """
    return Membership.objects.create(
        title="Fake Membership", active_months=6, is_available=True
    )


@pytest.fixture
def create_subscription(create_membership, user):
    """
    Create a subscription
    """
    return Subscription.objects.create(
        user=user,
        membership=create_membership,
    )


@pytest.fixture
def create_premium_user(create_subscription):
    return create_subscription.user
