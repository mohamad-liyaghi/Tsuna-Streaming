import pytest
from viewers.models import Viewer
from accounts.models import Account
from channels.models import Channel


@pytest.mark.django_db
def test_create_viewer(viewer):
    assert Viewer.objects.count() == 1


@pytest.mark.django_db
def test_create_cached_viewer(cached_viewer):
    user = Account.objects.get(id=cached_viewer["user"])
    channel = Channel.objects.get(id=cached_viewer["channel"])
    assert (
        Viewer.objects.get_from_cache(
            user=user,
            channel=channel,
            content_object=cached_viewer["content_object"],
        )
        is not None
    )
