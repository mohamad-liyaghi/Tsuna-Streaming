import pytest
from channel_admins.models import ChannelAdmin


@pytest.mark.django_db
class TestSignals:
    def test_create_admin_after_creating_channel(self, create_channel):
        assert ChannelAdmin.objects.count() == 1

    def test_delete_admin_after_unsubscribing(self, create_channel_admin):
        assert ChannelAdmin.objects.count() == 2
        create_channel_admin.channel.subscribers.all().delete()
        assert ChannelAdmin.objects.count() == 0

    def test_create_permissions_for_admin(self, create_channel_admin):
        assert create_channel_admin.permissions is not None
        assert create_channel_admin.permissions.admin == create_channel_admin
