import pytest
from faker import Faker
from accounts.models import Account

# Create a Faker object
faker = Faker()


@pytest.fixture
def create_deactive_user():
    """A fixture to create a deactive user"""
    user = Account.objects.create_user(
        email=faker.email(),
        password=faker.password(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )
    user.is_active = False
    user.save()
    return user


@pytest.fixture
def create_active_user():
    """A fixture to create an active user"""
    user = Account.objects.create_user(
        email=faker.email(),
        password=faker.password(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def create_superuser():
    """A fixture to create a superuser"""
    return Account.objects.create_superuser(
        email=faker.email(),
        password=faker.password(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )

