from django.core.exceptions import PermissionDenied
from channels.models import Channel
from channels.exceptions import ChannelLimitExceededException
import pytest


@pytest.mark.django_db
class TestChannelModel:
    def test_create_channel_by_inactive_user_fails(self, inactive_user):
        with pytest.raises(PermissionDenied):
            Channel.objects.create(owner=inactive_user, title="test")

    def test_create_channel_by_superuser(self, superuser):
        Channel.objects.create(owner=superuser, title="test")
        assert superuser.channels.count() == 1

    def test_create_channel_by_normal_user(self, user):
        for _ in range(1, 6):
            Channel.objects.create(owner=user, title="test")
        assert user.channels.count() == 5

    def test_channel_limit_for_superuser(self, superuser):
        for _ in range(1, 12):
            Channel.objects.create(owner=superuser, title="test")
        assert superuser.channels.count() == 11
        assert superuser.is_admin()

    def test_channel_limit_for_premium_user(self, premium_user):
        for _ in range(1, 11):
            Channel.objects.create(owner=premium_user, title="test")

        assert premium_user.channels.count() == 10
        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=premium_user, title="test")

    def test_channel_limit_for_normal_user(self, another_user):
        for _ in range(1, 6):
            Channel.objects.create(owner=another_user, title="test")

        assert another_user.channels.count() == 5
        with pytest.raises(ChannelLimitExceededException):
            Channel.objects.create(owner=another_user, title="test")

    def test_channel_limit_for_former_premium_user(self, premium_user):
        assert premium_user.is_premium()
        for _ in range(1, 11):
            Channel.objects.create(owner=premium_user, title="test")

        assert premium_user.channels.count() == 10

        premium_user.channels.first().delete()
        assert premium_user.channels.count() == 9

        premium_user.subscriptions.first().delete()
        assert premium_user.is_normal()

        Channel.objects.create(owner=premium_user, title="test")
        assert premium_user.channels.count() == 10
