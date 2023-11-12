import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.fixture(scope="class")
def subscriber(django_db_setup, django_db_blocker, channel, superuser):
    with django_db_blocker.unblock():
        yield ChannelSubscriber.objects.create(user=superuser, channel=channel)


@pytest.fixture(scope="class")
def cached_subscriber(channel, superuser, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield ChannelSubscriber.objects.create_in_cache(channel=channel, user=superuser)
