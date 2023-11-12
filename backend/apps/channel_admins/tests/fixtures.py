import pytest
from channel_admins.models import ChannelAdmin


@pytest.fixture(scope="class")
def channel_admin(channel, subscriber, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield ChannelAdmin.objects.create(
            user=subscriber.user,
            channel=channel,
            promoted_by=channel.owner,
        )
