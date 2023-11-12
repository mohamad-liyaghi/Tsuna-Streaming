from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
import pytest
from videos.models import Video
from videos.constants import VIDEO_LIMIT_NORMAL_USER, VIDEO_LIMIT_PREMIUM_USER
from core.utils import get_content_type_model
from votes.models import Vote, VoteChoice
from comments.models import Comment
from viewers.models import Viewer
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestVideoModel:
    def test_get_vide_content_type_id(self, video):
        # Get from db
        video_content_type_id = ContentType.objects.get_for_model(type(video)).id

        # Assert with the method
        assert get_content_type_model(model=type(video)).id == video_content_type_id

    def test_get_video_content_type_model(self, video):
        video_content_type = ContentType.objects.get_for_model(type(video))
        assert get_content_type_model(model=type(video)) == video_content_type

        # second time, get from cache
        video_content_type = ContentType.objects.get_for_model(type(video))
        assert get_content_type_model(model=type(video)) == video_content_type

    def test_get_video_views(self, video):
        """
        By default, video has 0 views
        """
        assert (
            Viewer.objects.get_count(content_object=video, channel=video.channel) == 0
        )

    def test_published_method(self, video):
        video.visibility = ContentVisibility.PUBLISHED
        video.save()
        video.refresh_from_db()

        assert Video.objects.published().filter(id=video.id).exists()

    def test_delete_votes_after_deleting_video(self, video):
        """
        Delete votes after deleting the video
        """
        assert Vote.objects.count() == 0

        Vote.objects.create(user=video.user, content_object=video)
        assert Vote.objects.count() == 1

        video.delete()
        assert Vote.objects.count() == 0

    def test_video_raise_admin_not_found(self, superuser, channel, create_file):
        """
        Raise error if non-admin wants to add video
        """
        with pytest.raises(PermissionDenied):
            Video.objects.create(
                title="test",
                description="new video",
                file=create_file,
                user=superuser,
                channel=channel,
            )

    def test_video_size_limit_premium_user(self, premium_user, channel, create_file):
        over_limit = int(VIDEO_LIMIT_PREMIUM_USER) + 100000000000000
        create_file.size = over_limit

        with pytest.raises(ValidationError):
            Video.objects.create(
                title="test",
                description="new video",
                file=create_file,
                user=premium_user,
                channel=channel,
            )

    def test_video_size_limit_normal_user(self, another_user, channel, create_file):
        over_limit = int(VIDEO_LIMIT_NORMAL_USER) + 100000000000000
        create_file.size = over_limit

        with pytest.raises(ValidationError):
            Video.objects.create(
                title="test",
                description="new video",
                file=create_file,
                user=another_user,
                channel=channel,
            )
