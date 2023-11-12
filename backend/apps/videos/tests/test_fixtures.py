import pytest
from videos.models import Video


@pytest.mark.django_db
def test_create_video(video):
    assert Video.objects.filter(id=video.id).count() == 1
