import pytest
from channels.models import Channel
from accounts.models import Account
from votes.models import Vote


@pytest.mark.django_db
class TestDeleteInCache:
    def test_delete_db_vote_in_cache(self, create_vote):
        channel = create_vote.channel

        Vote.objects.delete_in_cache(
            channel=channel,
            user=create_vote.user,
            content_object=create_vote.content_object,
        )
        assert (
            Vote.objects.get_count(
                channel=channel,
                content_object=create_vote.content_object,
            )
            == 0
        )

    def test_delete_cached_vote(self, create_cached_vote):
        channel = Channel.objects.get(id=create_cached_vote["channel"])
        user = Account.objects.get(id=create_cached_vote["user"])
        content_object = create_cached_vote["content_object"]

        Vote.objects.delete_in_cache(
            channel=channel,
            user=user,
            content_object=content_object,
        )
        assert (
            Vote.objects.get_count(
                channel=channel,
                content_object=content_object,
            )
            == 0
        )

    def test_delete_invalid_vote_in_cache(
        self, create_superuser, create_channel, create_video
    ):
        with pytest.raises(ValueError):
            Vote.objects.delete_in_cache(
                channel=create_channel,
                user=create_superuser,
                content_object=create_video,
            )
