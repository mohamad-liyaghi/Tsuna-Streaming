import pytest
from votes.models import Vote


@pytest.mark.django_db
def test_create_vote(create_vote):
    assert Vote.objects.count() == 1
