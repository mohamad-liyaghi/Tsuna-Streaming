import pytest
from viewers.models import Viewer
from channels.models import Channel


@pytest.mark.django_db
class TestViewerCount:
    def test_get_cached_viewer(self, create_cached_viewer):
        channel = Channel.objects.get(id=create_cached_viewer['channel'])
        assert Viewer.objects.get_count(
            channel=channel, content_object=create_cached_viewer['content_object']
        ) == 1

    def test_get_count_in_db(self, create_viewer):
        assert Viewer.objects.get_count(
            channel=create_viewer.channel,
            content_object=create_viewer.content_object
        ) == 1

    def test_get_count_null(self, create_video):
        assert Viewer.objects.get_count(
            channel=create_video.channel, content_object=create_video
        ) == 0
