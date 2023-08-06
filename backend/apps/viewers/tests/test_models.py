import pytest
from viewers.models import Viewer


@pytest.mark.django_db
class TestViewerModel:

    def test_delete_viewer_after_deleting_object(self, create_viewer):
        assert Viewer.objects.count() == 1
        create_viewer.content_object.delete()
        assert Viewer.objects.count() == 0

    def test_set_channel(self, create_viewer):
        """
        When a viewer is created,
        the channel field should be set to the channel of the video.
        """
        assert Viewer.objects.count() == 1
        assert create_viewer.channel == create_viewer.content_object.channel