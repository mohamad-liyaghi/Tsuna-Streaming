import pytest
from accounts.models import Account
from accounts.tests.utils import user_credentials


@pytest.fixture(scope="class")
def inactive_user(django_db_setup, django_db_blocker) -> Account:
    """A fixture to create a inactive user"""
    with django_db_blocker.unblock():
        yield Account.objects.create_user(**user_credentials(), is_active=False)


@pytest.fixture(scope="class")
def user(django_db_setup, django_db_blocker) -> Account:
    """A fixture to create an active user"""
    with django_db_blocker.unblock():
        yield Account.objects.create_user(**user_credentials(), is_active=True)


@pytest.fixture(scope="class")
def another_user(django_db_setup, django_db_blocker) -> Account:
    """A fixture to create an active user"""
    with django_db_blocker.unblock():
        yield Account.objects.create_user(**user_credentials(), is_active=True)


@pytest.fixture(scope="class")
def superuser(django_db_setup, django_db_blocker) -> Account:
    """A fixture to create a superuser"""
    with django_db_blocker.unblock():
        yield Account.objects.create_superuser(**user_credentials())


@pytest.fixture(scope="class")
def premium_user(subscription, django_db_blocker, django_db_setup):
    with django_db_blocker.unblock():
        yield subscription.user
