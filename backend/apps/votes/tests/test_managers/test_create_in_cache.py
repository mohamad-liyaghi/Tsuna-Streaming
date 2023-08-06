import pytest
from votes.models import Vote


@pytest.mark.django_db
class TestCreateInCache:
    def test_create_cached_vote(self, create_channel, create_superuser, create_video):
        Vote.objects.create_in_cache(
            channel=create_channel,
            user=create_superuser,
            content_object=create_video,
        )
        assert Vote.objects.get_count(
            channel=create_channel,
            content_object=create_video,
        ) == 1

    def test_create_cached_vote_twice(self, create_channel, create_superuser, create_video):
        Vote.objects.create_in_cache(
            channel=create_channel,
            user=create_superuser,
            content_object=create_video,
        )
        # Second Time
        Vote.objects.create_in_cache(
            channel=create_channel,
            user=create_superuser,
            content_object=create_video,
        )
        assert Vote.objects.get_count(
            channel=create_channel,
            content_object=create_video,
        ) == 1
