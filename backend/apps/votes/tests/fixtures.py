import pytest
from votes.models import Vote


@pytest.fixture(scope="class")
def vote(superuser, video, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return Vote.objects.create(user=superuser, content_object=video)


@pytest.fixture()
def cached_vote(superuser, video, channel):
    return Vote.objects.create_in_cache(
        user=superuser, channel=channel, content_object=video
    )
