from comments.models import Comment
from comments.exceptions import CommentNotAllowed
import pytest


@pytest.mark.django_db
class TestCommentModel:
    def test_update_comment(self, comment, video):
        """
        When a comment is updated, edited field should be set to True
        """

        assert not comment.edited

        comment.body = "Updated body"
        comment.save()
        comment.refresh_from_db()

        assert comment.edited

    def test_raise_exception_comment_not_allowed(self, video):
        """
        Raise exception when comments are not allowed for object
        and user tries to create a comment
        """

        video.allow_comment = False
        video.save()

        with pytest.raises(CommentNotAllowed):
            Comment.objects.create(content_object=video, user=video.user, body="test")

    def test_delete_comments_after_deleting_video(self, comment, video):
        """
        Ensure that comments are deleted after deleting the video
        """
        video_id = video.id
        video.delete()
        assert Comment.objects.filter(object_id=video_id).count() == 0
