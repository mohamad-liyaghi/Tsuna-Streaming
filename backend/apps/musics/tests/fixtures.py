import pytest
from musics.models import Music
from contents.models import ContentVisibility


@pytest.fixture(scope="class")
def music(channel, create_file, django_db_blocker, django_db_setup):
    with django_db_blocker.unblock():
        yield Music.objects.create(
            title="test",
            user=channel.owner,
            channel=channel,
            file=create_file,
            visibility=ContentVisibility.PUBLISHED,
        )
