from django.db.utils import IntegrityError
import pytest
from votes.models import Vote


@pytest.mark.django_db
class TestVoteModel:
    def test_delete_votes_after_deleting_video(self, create_vote):
        """
        After deleting an objects, its votes should be deleted too.
        """
        assert Vote.objects.count() == 1
        create_vote.content_object.delete()
        assert Vote.objects.count() == 0

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

    # TODO: write this tests
    # def test_get_object_votes_count(self):
    #     '''test get video votes count'''
    #     self.create_video()

    #     assert cache.get(f"vote_count:{self.video.token}") is None
    #     assert self.video.get_votes_count()['upvotes'] == 0

    #     Vote.objects.create(content_object=self.video, user=self.user, choice='u')
    #     assert cache.get(f"vote_count:{self.video.token}") is not None
    #     cache.delete(f"vote_count:{self.video.token}")
    #     assert self.video.get_votes_count()['upvotes'] == 1
