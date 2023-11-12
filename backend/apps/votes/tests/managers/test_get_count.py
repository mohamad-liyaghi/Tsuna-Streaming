import pytest
from votes.models import Vote
from channels.models import Channel


@pytest.mark.django_db
class TestVoteCount:
    def test_get_vote_cached(self, cached_vote):
        channel = Channel.objects.get(id=cached_vote["channel"])
        assert (
            Vote.objects.get_count(
                channel=channel, content_object=cached_vote["content_object"]
            )
            == 1
        )

    def test_get_count_in_db(self, vote):
        assert (
            Vote.objects.get_count(
                channel=vote.channel, content_object=vote.content_object
            )
            == 1
        )

    def test_get_count(self, video):
        assert Vote.objects.get_count(channel=video.channel, content_object=video) == 1
