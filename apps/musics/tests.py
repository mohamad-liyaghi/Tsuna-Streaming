from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
import pytest
from accounts.models import Account
from channels.models import Channel
from musics.models import Music
from votes.models import Vote, VoteChoice
from comments.models import Comment
from viewers.models import Viewer
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestMusicModel:
    def create_music(self):
        self.music = Music.objects.create(title='test', description='new music', 
                                        file='music.mp3', user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.user.is_active = True
        self.user.save()
        self.channel = Channel.objects.create(owner=self.user, title="test")    
    

    def test_create_music(self):

        '''Simply create a music'''
        self.create_music()
        assert self.channel.musics.count() == 1
    

    def test_get_music_content_type_id(self):
        self.create_music()
        cls = self.music.__class__
        music_content_type_id = ContentType.objects.get_for_model(cls).id

        assert get_content_type_model(
            model=self.music.__class__,
            return_id=True
        ) == music_content_type_id


    def test_get_music_content_type_model(self):
        self.create_music()
        cls = self.music.__class__
        music_content_type = ContentType.objects.get_for_model(cls)
        assert get_content_type_model(model=Music) == music_content_type

        # second time, get from cache
        music_content_type = ContentType.objects.get_for_model(cls)
        assert get_content_type_model(model=Music) == music_content_type


    # TODO: write this tests
    # def test_get_music_views(self):
    #     '''Test the get_viewer_count placed in AbstractContent'''
    #     self.create_music()

    #     assert self.music.get_viewer_count() == 0


    def test_delete_vote_after_deleting_music(self):

        '''There is a signal that deletes all votes related to a deleted object'''
        self.create_music()
        assert self.music.votes.count() == 0

        Vote.objects.create(user=self.user, choice=VoteChoice.UPVOTE, content_object=self.music)
        assert self.music.votes.count() == 1

        self.music.delete()
        assert self.music.votes.count() == 0
    
    def test_delete_comment_after_deleting_music(self):
        '''There is a signal that deletes all comments related to a deleted object'''

        self.create_music()
        assert self.music.comments.count() == 0

        Comment.objects.create(user=self.user, content_object=self.music, body="Test comment")

        assert self.music.comments.count() == 1

        self.music.delete()
        assert self.music.comments.count() == 0
    
    def test_delete_viewer_after_deleting_music(self):
        '''There is a signal that deletes all comments related to a deleted object'''

        self.create_music()
        assert self.music.viewers.count() == 0

        Viewer.objects.create(user=self.user, content_object=self.music)

        assert self.music.viewers.count() == 1

        self.music.delete()
        assert self.music.viewers.count() == 0


    def test_music_raise_admin_not_found(self):
        '''When user is not admin and wants to add music, it gets AdminNotFount'''
        non_admin_user = Account.objects.create_user(email='nontadmin@not.com', password='1234TEst')

        with pytest.raises(PermissionDenied):
            self.music = Music.objects.create(title='test', description='new music', 
                                        file='music.mp3', user=non_admin_user, channel=self.channel)
