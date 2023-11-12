import pytest
from channels.models import Channel


@pytest.fixture(scope="class")
def channel(user, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield Channel.objects.create(title="test", owner=user)
