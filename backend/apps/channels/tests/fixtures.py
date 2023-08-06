import pytest
from channels.models import Channel


@pytest.fixture
def create_channel(create_active_user):
    """
    Creates a channel.
    """
    return Channel.objects.create(
        title="test",
        owner=create_active_user
    )

