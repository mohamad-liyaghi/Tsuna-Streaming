from django.db.utils import IntegrityError
import pytest
from votes.models import Vote
from channels.models import Channel


@pytest.mark.django_db
class TestVoteModel:
    def test_set_channel_for_vote(self, create_vote):
        assert create_vote.channel == create_vote.content_object.channel

    def test_vote_token(self, create_vote):
        assert create_vote.token

    def test_vote_uniqueness(self, create_vote):
        """
        Users can only vote to an object once
        """
        with pytest.raises(IntegrityError):
            Vote.objects.create(
                user=create_vote.user,
                content_object=create_vote.content_object
            )

    def test_get_object_votes_count_no_vote(self, create_video):
        """
        Get count of an objects votes.
        """

        votes_count = Vote.objects.get_count(
            content_object=create_video.channel, channel=create_video.channel
        )
        assert votes_count == 0

    def test_get_object_votes_count_vote_in_db(self, create_video, create_vote):

        votes_count = Vote.objects.get_count(
            content_object=create_video.channel, channel=create_video.channel
        )
        assert votes_count == 1

    def test_get_object_votes_count_vote_in_cache(self, create_cached_vote):
        channel = Channel.objects.get(id=create_cached_vote['channel'])

        votes_count = Vote.objects.get_count(
            content_object=create_cached_vote['content_object'], channel=channel
        )
        assert votes_count == 1
