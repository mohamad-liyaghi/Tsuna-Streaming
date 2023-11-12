import pytest
from channels.models import Channel
from accounts.models import Account
from votes.models import Vote


@pytest.mark.django_db
class TestDeleteInCache:
    def test_delete_db_vote_in_cache(self, vote):
        channel = vote.channel

        Vote.objects.delete_in_cache(
            channel=channel,
            user=vote.user,
            content_object=vote.content_object,
        )
        assert (
            Vote.objects.get_count(
                channel=channel,
                content_object=vote.content_object,
            )
            == 0
        )

    def test_delete_cached_vote(self, cached_vote):
        channel = Channel.objects.get(id=cached_vote["channel"])
        user = Account.objects.get(id=cached_vote["user"])
        content_object = cached_vote["content_object"]

        Vote.objects.delete_in_cache(
            channel=channel,
            user=user,
            content_object=content_object,
        )
        assert Vote.objects.get_count(
            channel=channel,
            content_object=content_object,
        )
