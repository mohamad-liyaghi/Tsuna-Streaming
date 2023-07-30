import pytest
from viewers.models import Viewer


@pytest.mark.django_db
def test_create_viewer(create_viewer):
    assert Viewer.objects.count() == 1
