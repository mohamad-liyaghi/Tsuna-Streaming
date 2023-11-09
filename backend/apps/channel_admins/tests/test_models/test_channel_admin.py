import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import PermissionDenied
from channel_admins.models import ChannelAdmin
from channel_admins.exceptions import SubscriptionRequiredException
from accounts.models import Account
from channels.models import Channel


@pytest.mark.django_db
class TestAdminModel:
    def test_create_channel(self, create_channel, create_subscriber):
        ChannelAdmin.objects.create(
            user=create_subscriber.user,
            channel=create_channel,
            promoted_by=create_channel.owner,
        )

    def test_create_channel_admin_twice(self, create_channel):
        with pytest.raises(IntegrityError):
            ChannelAdmin.objects.create(
                user=create_channel.owner,
                channel=create_channel,
                promoted_by=create_channel.owner,
            )

    def test_create_no_subscription(self, create_channel, create_superuser):
        with pytest.raises(SubscriptionRequiredException):
            ChannelAdmin.objects.create(
                user=create_superuser,
                channel=create_channel,
                promoted_by=create_channel.owner,
            )

    def test_create_subscription_in_cache(self, create_cached_subscriber):
        channel = Channel.objects.get(id=create_cached_subscriber["channel"])
        user = Account.objects.get(id=create_cached_subscriber["user"])
        with pytest.raises(SubscriptionRequiredException):
            ChannelAdmin.objects.create(
                user=user, channel=channel, promoted_by=channel.owner
            )

    def test_promote_by_non_owner(
        self,
        create_channel,
        create_channel_admin,
    ):
        with pytest.raises(PermissionDenied):
            ChannelAdmin.objects.create(
                user=create_channel_admin.user,
                channel=create_channel,
                promoted_by=create_channel_admin.user,
            )
