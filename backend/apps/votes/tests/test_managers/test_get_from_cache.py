import pytest
from votes.models import Vote
from channels.models import Channel
from accounts.models import Account

@pytest.mark.django_db
class TestGetVoteFromCache:
    def test_get_cached(self, create_cached_vote):
        vote = Vote.objects.get_from_cache(
            channel=Channel.objects.get(id=create_cached_vote['channel']),
            user=Account.objects.get(id=create_cached_vote['user']),
            content_object=create_cached_vote['content_object']
        )
        assert vote['source'] == 'cache'

    def test_get_from_db(self, create_vote):
        vote = Vote.objects.get_from_cache(
            channel=create_vote.channel,
            user=create_vote.user,
            content_object=create_vote.content_object
        )
        assert vote['source'] == 'database'
