import pytest
from channel_admins.models import ChannelAdmin


@pytest.fixture
def create_channel_admin(channel, create_subscriber):
    """
    Create a new channel admin
    """
    return ChannelAdmin.objects.create(
        user=create_subscriber.user,
        channel=channel,
        promoted_by=channel.owner,
    )
