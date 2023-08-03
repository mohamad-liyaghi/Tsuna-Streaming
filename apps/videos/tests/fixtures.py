import pytest
from videos.models import Video


@pytest.fixture
def create_video(create_channel, create_file):
    return Video.objects.create(
        title='test', user=create_channel.owner,
        channel=create_channel, file=create_file
    )
