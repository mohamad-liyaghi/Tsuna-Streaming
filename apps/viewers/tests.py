from channels.models import Channel
from videos.models import Video
from accounts.models import Account
from viewers.models import Viewer

import pytest


@pytest.mark.django_db
class TestViewerModel:
    def create_video(self):
        self.video = Video.objects.create(title='test', description='new video', 
                                        file='fake_video.mp4', user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="test")    


    def test_delete_viewers_after_deleting_video(self):
        '''After deleting a video, all related viewers will be deleted'''

        self.create_video()

        assert Viewer.objects.count() == 0
        Viewer.objects.create(content_object=self.video, user=self.user)
        assert Viewer.objects.count() == 1

        self.video.delete()
        assert Viewer.objects.count() == 0
        assert Viewer.objects.count() != 1