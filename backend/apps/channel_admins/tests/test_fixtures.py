import pytest
from channel_admins.models import ChannelAdmin

@pytest.mark.django_db
def test_create_channel_admin(create_channel_admin):
    assert ChannelAdmin.objects.count() == 2
