import pytest
from videos.models import Video


@pytest.mark.django_db
def test_create_video(create_video):
    assert Video.objects.count() == 1