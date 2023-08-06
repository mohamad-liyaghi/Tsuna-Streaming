import pytest
from musics.models import Music
from contents.models import ContentVisibility


@pytest.fixture
def create_music(create_channel, create_file):
    return Music.objects.create(
        title='test', user=create_channel.owner,
        channel=create_channel, file=create_file,
        visibility=ContentVisibility.PUBLISHED
    )
