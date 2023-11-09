import pytest
from votes.models import Vote
from videos.models import Video


@pytest.fixture
def create_vote(create_superuser, create_channel, create_video):
    return Vote.objects.create(user=create_superuser, content_object=create_video)


@pytest.fixture
def create_cached_vote(create_superuser, create_channel, create_video):
    return Vote.objects.create_in_cache(
        user=create_superuser, channel=create_channel, content_object=create_video
    )
