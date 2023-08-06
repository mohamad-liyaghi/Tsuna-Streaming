import pytest
from django.db.utils import IntegrityError
from channel_admins.models import ChannelAdmin, ChannelAdminPermission


@pytest.mark.django_db
class TestAdminPermissionModel:
    def test_channel_owner_permission(self, create_channel):
        """
        For channel owners, all the permissions must be True.
        """
        permission = create_channel.owner.channel_admins.first().permissions
        assert permission.can_add_object is True
        assert permission.can_edit_object is True
        assert permission.can_delete_object is True
        assert permission.can_publish_object is True

    def test_channel_admin_permission(self, create_channel_admin):
        """
        For channel admins, all the permissions must be False.
        """
        permission = create_channel_admin.permissions
        assert permission.can_add_object is False
        assert permission.can_edit_object is False
        assert permission.can_delete_object is False
        assert permission.can_publish_object is False

    def test_create_permission_twice(self, create_channel_admin):
        with pytest.raises(IntegrityError):
            ChannelAdminPermission.objects.create(
                admin=create_channel_admin
            )
