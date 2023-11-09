import pytest
from votes.models import Vote
from channels.models import Channel


@pytest.mark.django_db
class TestVoteCount:
    def test_get_vote_cached(self, create_cached_vote):
        channel = Channel.objects.get(id=create_cached_vote["channel"])
        assert (
            Vote.objects.get_count(
                channel=channel, content_object=create_cached_vote["content_object"]
            )
            == 1
        )

    def test_get_count_in_db(self, create_vote):
        assert (
            Vote.objects.get_count(
                channel=create_vote.channel, content_object=create_vote.content_object
            )
            == 1
        )

    def test_get_count_null(self, create_video):
        assert (
            Vote.objects.get_count(
                channel=create_video.channel, content_object=create_video
            )
            == 0
        )
