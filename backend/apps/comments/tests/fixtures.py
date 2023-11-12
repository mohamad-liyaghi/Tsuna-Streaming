import pytest
from comments.models import Comment


@pytest.fixture(scope="class")
def comment(video, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return Comment.objects.create(
            user=video.user, body="This is a comment", content_object=video
        )
