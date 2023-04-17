from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from accounts.models import Account
from channels.models import Channel
from musics.models import Music
from votes.models import Vote
from comments.models import Comment
from viewers.models import Viewer
import pytest

@pytest.mark.django_db
class TestMusicModel:
    def create_music(self):
        self.music = Music.objects.create(title='test', description='new music', 
                                        music='music.mp3', user=self.user, channel=self.channel)

    def setup(self):
        self.user = Account.objects.create_user(email="simple@simple.com", password="1234USERnormal")
        self.channel = Channel.objects.create(owner=self.user, title="test")    
    

    def test_create_music(self):

        '''Simply create a music'''
        self.create_music()
        assert self.channel.musics.count() == 1
    

    def test_get_music_content_type_id(self):
        '''Test the get_model_content_type_id() placed in BaseContentModel'''

        self.create_music()
        cls = self.music.__class__
        music_content_type_id = ContentType.objects.get_for_model(cls).id

        assert self.music.get_model_content_type_id() == music_content_type_id


    def test_get_music_content_type_model(self):

        self.create_music()
        cls = self.music.__class__
        music_content_type = ContentType.objects.get_for_model(cls)
        assert Music.get_model_content_type() == music_content_type

        # second time, get from cache
        music_content_type = ContentType.objects.get_for_model(cls)
        assert Music.get_model_content_type() == music_content_type


    def test_get_music_views(self):
        '''Test the get_viewer_count placed in BaseContentModel'''
        self.create_music()

        assert self.music.get_viewer_count() == 0


    def test_delete_vote_after_deleting_music(self):

        '''There is a signal that deletes all votes related to a deleted object'''
        self.create_music()
        assert self.music.votes.count() == 0

        Vote.objects.create(user=self.user, choice=Vote.Choice.UPVOTE, content_object=self.music)
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
                                        music='music.mp3', user=non_admin_user, channel=self.channel)
    
    def test_music_token(self):
        '''Test that music is in the music token'''
        self.create_music()
        assert self.music.token.split('-')[0] == self.music.__class__.__name__.lower()