import pytest
from votes.models import Vote
from videos.models import Video


@pytest.fixture
def create_vote(create_superuser, create_channel):
    # TODO: replace with fixture
    video = Video.objects.create(
        channel=create_channel,
        user=create_channel.owner,
        title='Fake',
        file='fake.mp4'
    )
    return Vote.objects.create(
        user=create_superuser,
        content_object=video
    )
