import pytest
from channels.models import Channel


@pytest.mark.django_db
def test_create_channel(channel):
    assert Channel.objects.filter(id=channel.id).count() == 1
