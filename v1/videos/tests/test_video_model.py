from django.contrib.contenttypes.models import ContentType

from accounts.models import Account
from channels.models import Channel
from videos.models import Video

from PIL import Image
from glob import glob
from os import path
import pytest


image = [Image.open(jpg) for jpg in glob(path.join('tests', 'fake_video.webp'))]

@pytest.mark.django_db
class TestVideoAdminModel:
    def create_video(self):
        self.video = Video.objects.create(title='test', description='new video', 
                                        video=image, user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="test")    
    

    def test_create_video(self):
        '''Simply create a video'''
        self.create_video()
        assert self.channel.videos.count() == 1
    

    def test_get_video_content_type_id(self):
        '''Test the get_model_content_type_id() placed in BaseContentModel'''

        self.create_video()
        cls = self.video.__class__
        video_content_type_id = ContentType.objects.get_for_model(cls).id

        assert self.video.get_model_content_type_id() == video_content_type_id


    def test_get_video_views(self):
        '''Test the get_viewer_count() placed in BaseContentModel'''
        self.create_video()

        assert self.video.get_viewer_count() == 0

    def test_published_method(self):
        Video.objects.create(
            title='test', description='new video', 
            video=image, user=self.user, channel=self.channel,
            visibility=Video.Visibility.PUBLISHED)

        assert self.channel.videos.published().count() == 1