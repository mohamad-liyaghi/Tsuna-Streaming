import pytest
from viewers.models import Viewer


@pytest.mark.django_db
class TestCreateInCache:
    def test_create_cached_viewer(self, create_channel, create_superuser, create_video):
        Viewer.objects.create_in_cache(
            channel=create_channel,
            user=create_superuser,
            content_object=create_video,
        )
        assert (
            Viewer.objects.get_count(
                channel=create_channel,
                content_object=create_video,
            )
            == 1
        )

    def test_create_cached_viewer_twice(
        self, create_channel, create_superuser, create_video
    ):
        Viewer.objects.create_in_cache(
            channel=create_channel,
            user=create_superuser,
            content_object=create_video,
        )
        # Second Time
        Viewer.objects.create_in_cache(
            channel=create_channel,
            user=create_superuser,
            content_object=create_video,
        )
        assert (
            Viewer.objects.get_count(
                channel=create_channel,
                content_object=create_video,
            )
            == 1
        )
