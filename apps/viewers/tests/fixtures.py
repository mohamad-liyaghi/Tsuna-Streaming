import pytest
from viewers.models import Viewer


@pytest.fixture
def create_viewer(create_video):
    return Viewer.objects.create(
        user=create_video.channel.owner,
        content_object=create_video
    )

# TOOD: create cached viewer