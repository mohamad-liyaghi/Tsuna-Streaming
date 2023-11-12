import pytest
from votes.models import Vote
from core.utils import ObjectSource
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestGetVoteFromCache:
    def test_get_from_db(self, vote):
        vote = Vote.objects.get_from_cache(
            channel=vote.channel,
            user=vote.user,
            content_object=vote.content_object,
        )
        assert vote.get("source") == ObjectSource.DATABASE.value
