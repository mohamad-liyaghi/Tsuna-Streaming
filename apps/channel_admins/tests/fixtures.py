import pytest
from channel_admins.models import ChannelAdmin


@pytest.fixture
def create_channel_admin(create_channel, create_subscriber):
    """
    Create a new channel admin
    """
    return ChannelAdmin.objects.create(
        user=create_subscriber.user,
        channel=create_channel,
        promoted_by=create_channel.owner
    )
