from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from core.utils import get_content_type_model
from accounts.models import Account
from channels.models import Channel
from videos.models import Video
from votes.models import Vote, VoteChoice
from comments.models import Comment
from viewers.models import Viewer
from core.models import ContentVisibility


from PIL import Image
from glob import glob
from os import path
import pytest


image = [Image.open(jpg) for jpg in glob(path.join('tests', 'fake_video.webp'))]

@pytest.mark.django_db
class TestVideoModel:
    def create_video(self):
        self.video = Video.objects.create(title='test', description='new video', 
                                        file=image, user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.user.is_active = True
        self.user.save()
        self.channel = Channel.objects.create(owner=self.user, title="test")    
    

    def test_create_video(self):
        '''Simply create a video'''
        self.create_video()
        assert self.channel.videos.count() == 1
    

    def test_get_video_content_type_id(self):

        self.create_video()
        cls = self.video.__class__
        video_content_type_id = ContentType.objects.get_for_model(cls).id

        assert get_content_type_model(
            self.video.__class__, return_id=True
        ) == video_content_type_id


    def test_get_video_content_type_model(self):

        self.create_video()
        cls = self.video.__class__
        video_content_type = ContentType.objects.get_for_model(cls)
        assert get_content_type_model(Video) == video_content_type

        # second time, get from cache
        video_content_type = ContentType.objects.get_for_model(cls)
        assert get_content_type_model(Video) == video_content_type


    def test_get_video_views(self):
        """
        By default, video has 0 views
        """
        self.create_video()

        assert Viewer.objects.get_count(
            content_object=self.video,
            channel=self.video.channel
        ) == 0

    def test_published_method(self):
        Video.objects.create(
            title='test', description='new video', 
            file=image, user=self.user, channel=self.channel,
            visibility=ContentVisibility.PUBLISHED)

        assert self.channel.videos.published().count() == 1


    def test_delete_vote_after_deleting_video(self):
        '''There is a signal that deletes all votes related to a deleted object'''
        self.create_video()
        assert self.video.votes.count() == 0

        Vote.objects.create(user=self.user, choice=VoteChoice.UPVOTE, content_object=self.video)
        assert self.video.votes.count() == 1

        self.video.delete()
        assert self.video.votes.count() == 0
    
    def test_delete_comment_after_deleting_video(self):
        '''There is a signal that deletes all comments related to a deleted object'''

        self.create_video()
        assert self.video.comments.count() == 0

        Comment.objects.create(user=self.user, content_object=self.video, body="Test comment")

        assert self.video.comments.count() == 1

        self.video.delete()
        assert self.video.comments.count() == 0
    
    def test_delete_viewer_after_deleting_video(self):
        '''There is a signal that deletes all comments related to a deleted object'''

        self.create_video()
        assert self.video.viewers.count() == 0

        Viewer.objects.create(user=self.user, content_object=self.video)

        assert self.video.viewers.count() == 1

        self.video.delete()
        assert self.video.viewers.count() == 0

    def test_video_raise_admin_not_found(self):
        '''When user is not admin and wants to add video, it gets AdminNotFount'''
        non_admin_user = Account.objects.create_user(email='nontadmin@not.com', password='1234TEst')

        with pytest.raises(PermissionDenied):
            self.video = Video.objects.create(title='test', description='new video', 
                                        file=image, user=non_admin_user, channel=self.channel)
