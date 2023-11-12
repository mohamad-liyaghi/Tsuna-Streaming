import pytest
from videos.models import Video
from contents.models import ContentVisibility


@pytest.fixture(scope="class")
def video(channel, create_file, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield Video.objects.create(
            title="test",
            user=channel.owner,
            channel=channel,
            file=create_file,
            visibility=ContentVisibility.PUBLISHED,
        )
