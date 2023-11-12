import pytest
from viewers.models import Viewer


@pytest.mark.django_db
class TestViewerModel:
    def test_set_channel(self, viewer):
        """
        When a viewer is created,
        the channel field should be set to the channel of the video.
        """
        assert Viewer.objects.filter(id=viewer.id).count() == 1
        assert viewer.channel == viewer.content_object.channel

    def test_delete_viewer_after_deleting_object(self, viewer):
        viewer_id = viewer.id
        viewer.content_object.delete()
        assert Viewer.objects.filter(id=viewer_id).count() == 0
