from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
import pytest
from musics.models import Music
from musics.constants import MUSIC_LIMIT_NORMAL_USER, MUSIC_LIMIT_PREMIUM_USER
from core.utils import get_content_type_model
from votes.models import Vote, VoteChoice
from comments.models import Comment
from viewers.models import Viewer
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestMusicModel:
    def test_get_vide_content_type_id(self, music):
        # Get from db
        music_content_type_id = ContentType.objects.get_for_model(type(music)).id

        # Assert with the method
        assert get_content_type_model(model=type(music)).id == music_content_type_id

    def test_get_music_content_type_model(self, music):
        music_content_type = ContentType.objects.get_for_model(type(music))
        assert get_content_type_model(model=type(music)) == music_content_type

        # second time, get from cache
        music_content_type = ContentType.objects.get_for_model(type(music))
        assert get_content_type_model(model=type(music)) == music_content_type

    def test_get_music_views(self, music):
        """
        By default, music has 0 views
        """

        assert (
            Viewer.objects.get_count(content_object=music, channel=music.channel) == 0
        )

    def test_published_method(self, music):
        music.visibility = ContentVisibility.PUBLISHED
        music.save()
        music.refresh_from_db()

        assert Music.objects.published().count() != 0

    def test_delete_votes_after_deleting_music(self, music):
        """
        Delete votes after deleting the music
        """
        assert Vote.objects.count() == 0

        Vote.objects.create(user=music.user, content_object=music)
        assert Vote.objects.count() == 1

        music.delete()
        assert Vote.objects.count() == 0

    def test_music_raise_admin_not_found(self, superuser, channel, create_file):
        """
        Raise error if non-admin wants to add music
        """
        with pytest.raises(PermissionDenied):
            Music.objects.create(
                title="test",
                description="new music",
                file=create_file,
                user=superuser,
                channel=channel,
            )

    def test_music_size_limit_premium_user(self, premium_user, channel, create_file):
        over_limit = int(MUSIC_LIMIT_PREMIUM_USER) + 100000000000000
        create_file.size = over_limit

        with pytest.raises(ValidationError):
            Music.objects.create(
                title="test",
                description="new Music",
                file=create_file,
                user=premium_user,
                channel=channel,
            )

    def test_music_size_limit_normal_user(self, another_user, channel, create_file):
        over_limit = int(MUSIC_LIMIT_NORMAL_USER) + 100000000000000
        create_file.size = over_limit

        with pytest.raises(ValidationError):
            Music.objects.create(
                title="test",
                description="new music",
                file=create_file,
                user=another_user,
                channel=channel,
            )
