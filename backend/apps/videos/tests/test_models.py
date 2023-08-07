from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
import pytest
from videos.models import Video
from videos.constants import (
    VIDEO_LIMIT_NORMAL_USER,
    VIDEO_LIMIT_PREMIUM_USER
)
from core.utils import get_content_type_model
from votes.models import Vote, VoteChoice
from comments.models import Comment
from viewers.models import Viewer
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestVideoModel:

    def test_get_vide_content_type_id(self, create_video):
        # Get from db
        video_content_type_id = ContentType.objects.get_for_model(
            type(create_video)
        ).id

        # Assert with the method
        assert get_content_type_model(
            model=type(create_video)
        ).id == video_content_type_id

    def test_get_video_content_type_model(self, create_video):
        video_content_type = ContentType.objects.get_for_model(
            type(create_video)
        )
        assert get_content_type_model(
            model=type(create_video)
        ) == video_content_type

        # second time, get from cache
        video_content_type = ContentType.objects.get_for_model(
            type(create_video)
        )
        assert get_content_type_model(
            model=type(create_video)
        ) == video_content_type

    def test_get_video_views(self, create_video):
        """
        By default, video has 0 views
        """

        assert Viewer.objects.get_count(
            content_object=create_video,
            channel=create_video.channel
        ) == 0

    def test_published_method(self, create_video):
        create_video.visibility = ContentVisibility.PUBLISHED
        create_video.save()
        create_video.refresh_from_db()

        assert Video.objects.published().count() == 1

    def test_delete_votes_after_deleting_video(self, create_video):
        """
        Delete votes after deleting the video
        """
        assert Vote.objects.count() == 0

        Vote.objects.create(
            user=create_video.user,
            content_object=create_video
        )
        assert Vote.objects.count() == 1

        create_video.delete()
        assert Vote.objects.count() == 0

    def test_delete_comment_after_deleting_video(self, create_video):
        """
        Delete comments after deleting a video
        """

        assert Comment.objects.count() == 0

        Comment.objects.create(
            user=create_video.user,
            content_object=create_video,
            body="Test comment"
        )
        assert Comment.objects.count() == 1

        create_video.delete()
        assert Comment.objects.count() == 0

    def test_delete_viewer_after_deleting_video(self, create_video):
        """
        Delete viewer of an object after deletion
        """
        assert Viewer.objects.count() == 0

        Viewer.objects.create(user=create_video.user, content_object=create_video)
        assert Viewer.objects.count() == 1

        create_video.delete()
        assert Viewer.objects.count() == 0

    def test_video_raise_admin_not_found(
            self,
            create_superuser,
            create_channel,
            create_file
    ):
        """
        Raise error if non-admin wants to add video
        """
        with pytest.raises(PermissionDenied):
            Video.objects.create(
                title='test',
                description='new video',
                file=create_file,
                user=create_superuser,
                channel=create_channel
            )

    def test_video_size_limit_premium_user(
            self,
            create_premium_user,
            create_channel,
            create_file
    ):
        over_limit = int(VIDEO_LIMIT_PREMIUM_USER) + 100000000000000
        create_file.size = over_limit

        with pytest.raises(ValidationError):
            Video.objects.create(
                title='test',
                description='new video',
                file=create_file,
                user=create_premium_user,
                channel=create_channel
            )

    def test_video_size_limit_normal_user(
            self,
            create_active_user,
            create_channel,
            create_file
    ):
        over_limit = int(VIDEO_LIMIT_NORMAL_USER) + 100000000000000
        create_file.size = over_limit

        with pytest.raises(ValidationError):
            Video.objects.create(
                title='test',
                description='new video',
                file=create_file,
                user=create_active_user,
                channel=create_channel
            )
