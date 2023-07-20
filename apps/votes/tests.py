from django.core.cache import cache
from channels.models import Channel
from videos.models import Video
from accounts.models import Account
from votes.models import Vote

import pytest


@pytest.mark.django_db
class TestVoteModel:
    def create_video(self):
        self.video = Video.objects.create(title='test', description='new video', 
                                        file='fake_video.mp4', user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.user.is_active = True
        self.user.save()
        self.channel = Channel.objects.create(owner=self.user, title="test")    


    def test_delete_votes_after_deleting_video(self):
        '''After deleting a video, all related votes will be deleted'''

        self.create_video()

        assert Vote.objects.count() == 0
        Vote.objects.create(content_object=self.video, user=self.user)
        assert Vote.objects.count() == 1

        self.video.delete()
        assert Vote.objects.count() == 0
        assert Vote.objects.count() != 1


    def test_create_vote(self):
        self.create_video()

        assert Vote.objects.count() == 0
        Vote.objects.create(content_object=self.video, user=self.user)

        assert Vote.objects.count() == 1


    def test_delete_vote(self):
        '''If user request to save vote twice, it means that he wants to remove the vote.'''

        self.create_video()

        assert Vote.objects.count() == 0
        Vote.objects.create(content_object=self.video, user=self.user)
        assert Vote.objects.count() == 1

        Vote.objects.create(content_object=self.video, user=self.user)
        assert Vote.objects.count() == 0


    def test_update_vote(self):
        '''If user save 2 votes with diffrent value, the oldest vote will be updated.'''

        self.create_video()

        assert Vote.objects.count() == 0
        Vote.objects.create(content_object=self.video, user=self.user)
        assert Vote.objects.count() == 1

        Vote.objects.create(content_object=self.video, user=self.user, choice=Vote.Choice.DOWNVOTE)
        assert Vote.objects.count() == 1
        assert Vote.objects.filter(choice=Vote.Choice.DOWNVOTE).count() == 1

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
