import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import PermissionDenied
from channel_admins.models import ChannelAdmin
from channel_admins.exceptions import SubscriptionRequiredException
from accounts.models import Account
from channels.models import Channel


@pytest.mark.django_db
class TestAdminModel:
    def test_channel(self, channel, subscriber):
        ChannelAdmin.objects.create(
            user=subscriber.user, channel=channel, promoted_by=channel.owner
        )

    def test_create_channel_admin_twice_fails(self, channel):
        with pytest.raises(IntegrityError):
            ChannelAdmin.objects.create(
                user=channel.owner, channel=channel, promoted_by=channel.owner
            )

    def test_create_no_subscription_fails(self, channel, another_user):
        with pytest.raises(SubscriptionRequiredException):
            ChannelAdmin.objects.create(
                user=another_user, channel=channel, promoted_by=channel.owner
            )

    def test_promote_by_non_owner_fails(self, channel, channel_admin):
        with pytest.raises(PermissionDenied):
            ChannelAdmin.objects.create(
                user=channel_admin.user,
                channel=channel,
                promoted_by=channel_admin.user,
            )
