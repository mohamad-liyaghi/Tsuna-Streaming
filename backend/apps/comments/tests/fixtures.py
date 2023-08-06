import pytest
from comments.models import Comment


@pytest.fixture
def create_comment(create_video):
    """
    Create a comment for an object
    """
    video = create_video
    return Comment.objects.create(
        user=video.user,
        body="This is a comment",
        content_object=video
    )
