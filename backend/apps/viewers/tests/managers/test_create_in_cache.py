import pytest
from viewers.models import Viewer


@pytest.mark.django_db
class TestCreateInCache:
    def test_create_cached_viewer(self, channel, superuser, video):
        Viewer.objects.create_in_cache(
            channel=channel,
            user=superuser,
            content_object=video,
        )
        assert (
            Viewer.objects.get_count(
                channel=channel,
                content_object=video,
            )
            == 1
        )

    def test_create_cached_viewer_twice(self, channel, superuser, video):
        Viewer.objects.create_in_cache(
            channel=channel,
            user=superuser,
            content_object=video,
        )
        # Second Time
        Viewer.objects.create_in_cache(
            channel=channel,
            user=superuser,
            content_object=video,
        )
        assert (
            Viewer.objects.get_count(
                channel=channel,
                content_object=video,
            )
            == 1
        )
