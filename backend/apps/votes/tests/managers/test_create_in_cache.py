import pytest
from votes.models import Vote


@pytest.mark.django_db
class TestCreateInCache:
    def test_create_cached_vote(self, channel, superuser, video):
        Vote.objects.create_in_cache(
            channel=channel,
            user=superuser,
            content_object=video,
        )
        assert (
            Vote.objects.get_count(
                channel=channel,
                content_object=video,
            )
            == 1
        )

    def test_create_cached_vote_twice(self, channel, superuser, video):
        Vote.objects.create_in_cache(
            channel=channel,
            user=superuser,
            content_object=video,
        )
        # Second Time
        Vote.objects.create_in_cache(
            channel=channel,
            user=superuser,
            content_object=video,
        )
        assert (
            Vote.objects.get_count(
                channel=channel,
                content_object=video,
            )
            == 1
        )
