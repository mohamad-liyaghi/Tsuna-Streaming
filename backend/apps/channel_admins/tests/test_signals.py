import pytest
from channel_admins.models import ChannelAdmin


@pytest.mark.django_db
class TestSignals:
    def test_create_admin_after_creating_channel(self, channel):
        assert ChannelAdmin.objects.filter(channel=channel).exists()

    def test_delete_admin_after_unsubscribing(self, channel_admin):
        assert ChannelAdmin.objects.filter(channel=channel_admin.channel).exists()
        channel_admin.channel.subscribers.all().delete()
        assert not ChannelAdmin.objects.filter(channel=channel_admin.channel).exists()

    def test_create_permissions_for_admin(self, channel_admin):
        assert channel_admin.permissions is not None
        assert channel_admin.permissions.admin == channel_admin
