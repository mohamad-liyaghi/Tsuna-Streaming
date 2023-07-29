import pytest
from videos.models import Video

# TODO: Move this
@pytest.fixture
def create_video(create_channel):
    return Video.objects.create(
        title='test', user=create_channel.owner,
        channel=create_channel, file='fake.mp3'
    )