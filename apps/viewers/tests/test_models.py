import pytest
from viewers.models import Viewer


@pytest.mark.django_db
class TestViewerModel:

    def test_set_channel(self, create_viewer):
        """
        When a viewer is created,
        the channel field should be set to the channel of the video.
        """
        assert Viewer.objects.count() == 1
        assert create_viewer.channel == create_viewer.content_object.channel