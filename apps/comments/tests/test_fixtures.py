import pytest
from comments.models import Comment


@pytest.mark.django_db
def test_create_comment(create_comment):
    """
    Test if a comment can be created
    """
    assert Comment.objects.count() == 1
