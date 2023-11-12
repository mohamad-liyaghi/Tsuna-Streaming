import pytest
from viewers.models import Viewer
from channels.models import Channel


@pytest.mark.django_db
class TestViewerCount:
    def test_get_count_in_db(self, viewer):
        assert (
            Viewer.objects.get_count(
                channel=viewer.channel,
                content_object=viewer.content_object,
            )
            == 1
        )

    def test_get_count_null(self, video):
        assert Viewer.objects.get_count(channel=video.channel, content_object=video)
