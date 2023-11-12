import pytest
from memberships.models import Membership, Subscription


@pytest.fixture(scope="class")
def membership(django_db_setup, django_db_blocker) -> Membership:
    with django_db_blocker.unblock():
        yield Membership.objects.create(
            title="Fake Membership", active_months=6, is_available=True
        )


@pytest.fixture(scope="class")
def subscription(membership, user, django_db_blocker, django_db_setup):
    with django_db_blocker.unblock():
        yield Subscription.objects.create(
            user=user,
            membership=membership,
        )
