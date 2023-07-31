import pytest
from viewers.models import Viewer


@pytest.fixture
def create_viewer(create_video):
    return Viewer.objects.create(
        user=create_video.channel.owner,
        content_object=create_video
    )


@pytest.fixture
def create_cached_viewer(create_video):
    return Viewer.objects.create_in_cache(
        user=create_video.channel.owner,
        channel=create_video.channel,
        content_object=create_video
    )
