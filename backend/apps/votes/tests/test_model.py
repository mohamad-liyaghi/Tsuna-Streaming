from django.db.utils import IntegrityError
import pytest
from votes.models import Vote
from channels.models import Channel


@pytest.mark.django_db
class TestVoteModel:
    def test_set_channel_for_vote(self, vote):
        assert vote.channel == vote.content_object.channel

    def test_vote_token(self, vote):
        assert vote.token

    def test_vote_uniqueness(self, vote):
        """
        Users can only vote to an object once
        """
        with pytest.raises(IntegrityError):
            Vote.objects.create(user=vote.user, content_object=vote.content_object)

    def test_get_object_votes_count_no_vote(self, video):
        """
        Get count of an objects votes.
        """

        votes_count = Vote.objects.get_count(
            content_object=video.channel, channel=video.channel
        )
        assert votes_count == 0

    def test_get_object_votes_count_vote_in_db(self, video, vote):
        votes_count = Vote.objects.get_count(
            content_object=video, channel=video.channel
        )
        assert votes_count == 1
