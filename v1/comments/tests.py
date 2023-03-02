from channels.models import Channel
from videos.models import Video
from accounts.models import Account
from comments.models import Comment
from comments.exceptions import CommentNotAllowed
import pytest


@pytest.mark.django_db
class TestCommentModel:
    def create_video(self):
        self.video = Video.objects.create(title='test', description='new video', 
                                        video='fake_video.mp4', user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="test")    


    def test_delete_comments_after_deleting_video(self):
        '''After deleting a video, all related comments will be deleted'''

        self.create_video()

        assert Comment.objects.count() == 0
        Comment.objects.create(content_object=self.video, user=self.user, body='test')
        assert Comment.objects.count() == 1

        self.video.delete()
        assert Comment.objects.count() == 0
        assert Comment.objects.count() != 1


    def test_raise_exception_comment_not_allowed(self):
        '''raise exception when allow_comment is False and user wants to add comment'''

        self.create_video()
        # create a comment when allow_comment is True
        Comment.objects.create(content_object=self.video, user=self.user, body='test')

        # disallow comments
        self.video.allow_comment = False

        with pytest.raises(CommentNotAllowed):
    
            Comment.objects.create(content_object=self.video, user=self.user, body='test')


    def test_update_comment(self):
        '''When user update a comment, the edited field gets updated to True'''
        self.create_video()
        comment = Comment.objects.create(content_object=self.video, user=self.user, body='testd')
        
        comment.body='test'
        comment.save()
        assert comment.edited == True