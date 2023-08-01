from comments.models import Comment
from comments.exceptions import CommentNotAllowed
import pytest


@pytest.mark.django_db
class TestCommentModel:
    def test_delete_comments_after_deleting_video(self, create_comment):
        """
        Ensure that comments are deleted after deleting the video
        """
        assert Comment.objects.count() == 1
        # delete video
        create_comment.content_object.delete()
        assert Comment.objects.count() == 0

    def test_raise_exception_comment_not_allowed(self, create_video):
        """
        Raise exception when comments are not allowed for object
        and user tries to create a comment
        """

        create_video.allow_comment = False
        create_video.save()

        with pytest.raises(CommentNotAllowed):
            Comment.objects.create(
                content_object=create_video,
                user=create_video.user,
                body='test'
            )

    def test_update_comment(self, create_comment):
        """
        When a comment is updated, edited field should be set to True
        """
        assert not create_comment.edited

        create_comment.body = 'Updated body'
        create_comment.save()
        create_comment.refresh_from_db()

        assert create_comment.edited
