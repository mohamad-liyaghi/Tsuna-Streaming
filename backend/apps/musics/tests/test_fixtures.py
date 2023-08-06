import pytest
from musics.models import Music


@pytest.mark.django_db
def test_create_music(create_music):
    assert Music.objects.count() == 1
