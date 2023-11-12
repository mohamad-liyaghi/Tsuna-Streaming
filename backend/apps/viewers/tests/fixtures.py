import pytest
from viewers.models import Viewer


@pytest.fixture(scope="class")
def viewer(video):
    return Viewer.objects.create(user=video.channel.owner, content_object=video)


@pytest.fixture(scope="class")
def cached_viewer(video):
    return Viewer.objects.create_in_cache(
        user=video.channel.owner,
        channel=video.channel,
        content_object=video,
    )
