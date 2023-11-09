from django.core.exceptions import PermissionDenied
from channels.models import Channel
from channels.exceptions import ChannelLimitExceededException
import pytest


@pytest.mark.django_db
class TestChannelModel:
    def test_create_channel_by_inactive_user(self, create_deactive_user):
        """
        Inactive users can't create channels.
        """
        with pytest.raises(PermissionDenied):
            Channel.objects.create(owner=create_deactive_user, title="test")

    def test_create_channel_by_superuser(self, create_superuser):
        Channel.objects.create(owner=create_superuser, title="test")
        assert create_superuser.channels.count() == 1

    def test_create_channel_by_normal_user(self, create_active_user):
        """
        Normal users can only create 5 channels.
        """
        for _ in range(1, 6):
            Channel.objects.create(owner=create_active_user, title="test")
        assert create_active_user.channels.count() == 5

    def test_channel_limit_for_superuser(self, create_superuser):
        """Superusers has no limit in creating channels"""
        for _ in range(1, 12):
            Channel.objects.create(owner=create_superuser, title="test")
        assert create_superuser.channels.count() == 11
        assert create_superuser.is_admin()

    def test_channel_limit_for_premium_user(self, create_premium_user):
        """
        Premium users can create up to 10 channels.
        """

        for _ in range(1, 11):
            Channel.objects.create(owner=create_premium_user, title="test")

        assert create_premium_user.channels.count() == 10
        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=create_premium_user, title="test")

    def test_channel_limit_for_normal_user(self, create_active_user):
        """
        Normal users can create up to 5 channels.
        """
        for _ in range(1, 6):
            Channel.objects.create(owner=create_active_user, title="test")

        assert create_active_user.channels.count() == 5
        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=create_active_user, title="test")

    def test_channel_limit_for_former_premium_user(self, create_premium_user):
        """
        Former premium users can still create up to 10 channels.
        """
        assert create_premium_user.is_premium()
        for _ in range(1, 11):
            Channel.objects.create(owner=create_premium_user, title="test")

        assert create_premium_user.channels.count() == 10

        create_premium_user.channels.first().delete()
        assert create_premium_user.channels.count() == 9

        create_premium_user.subscriptions.first().delete()
        assert create_premium_user.is_normal()

        Channel.objects.create(owner=create_premium_user, title="test")
        assert create_premium_user.channels.count() == 10
