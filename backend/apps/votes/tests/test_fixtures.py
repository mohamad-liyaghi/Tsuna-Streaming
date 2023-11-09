import pytest
from votes.models import Vote
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
def test_create_vote(create_vote):
    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_create_vote_in_cache(create_cached_vote):
    user = Account.objects.get(id=create_cached_vote["user"])
    channel = Channel.objects.get(id=create_cached_vote["channel"])
    assert (
        Vote.objects.get_from_cache(
            user=user,
            channel=channel,
            content_object=create_cached_vote["content_object"],
        )
        is not None
    )
