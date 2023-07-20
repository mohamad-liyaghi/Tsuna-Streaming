import pytest


@pytest.mark.django_db
def test_create_subscriber(create_subscriber):
    assert create_subscriber.channel.subscribers.count() == 2
