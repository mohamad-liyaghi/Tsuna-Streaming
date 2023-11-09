from django.core.cache import cache
from django.db.models import Q
from celery import shared_task
from votes.models import Vote
from votes.constants import CACHE_OBJECT_VOTE
from accounts.models import Account
from core.utils import get_content_type_model
from core.utils import ObjectSource


@shared_task
def remove_object_votes(content_type_id: int, object_id: int, object_token: str):
    """
    Remove all objects votes
    """
    # get the object model content type (eg: Video)
    content_model = get_content_type_model(_id=content_type_id)

    # delete all related votes
    Vote.objects.filter(content_type=content_model, object_id=object_id).delete()
    # delete all related votes from cache
    cache.delete_pattern(
        CACHE_OBJECT_VOTE.format(
            channel_token="*", object_token=object_token, user_token="*"
        )
    )


@shared_task
def insert_vote_into_db():
    """
    Insert Cached votes to database.
    """
    # Get keys of all cached votes
    vote_keys = cache.keys(
        CACHE_OBJECT_VOTE.format(channel_token="*", object_token="*", user_token="*")
    )

    if vote_keys:
        # Get all cached votes
        all_votes = cache.get_many(vote_keys).values()

        # Filter those votes that are cached
        cached_votes = [
            vote
            for vote in all_votes
            if vote["source"] == ObjectSource.CACHE.value and not vote["pending_delete"]
        ]

        # Get all users of cached votes
        users = Account.objects.filter(id__in=[vote["user"] for vote in cached_votes])

        # Create instances of Vote model
        new_votes = [
            Vote(
                user=users.get(id=vote["user"]),
                content_object=vote["content_object"],
                choice=vote["choice"],
                date=vote["date"],
            )
            for vote in cached_votes
        ]

        # Bulk Insert
        Vote.objects.bulk_create(new_votes)
        # Delete their cache
        cache.delete_many(vote_keys)


@shared_task
def delete_unvoted_from_db():
    """
    Delete all unvoted objects from database.
    """
    # Get keys of all cached votes
    vote_keys = cache.keys(
        CACHE_OBJECT_VOTE.format(channel_token="*", object_token="*", user_token="*")
    )

    if vote_keys:
        # Get all cached votes
        all_votes = cache.get_many(vote_keys).values()

        # Filter those votes which are pending to delete
        pending_delete_votes = [vote for vote in all_votes if vote["pending_delete"]]
        # Get all users of cached votes
        users = Account.objects.filter(
            id__in=[vote["user"] for vote in pending_delete_votes]
        )

        content_models = [
            get_content_type_model(model=type(vote["content_object"]))
            for vote in pending_delete_votes
        ]
        content_object_ids = [
            vote["content_object"].id for vote in pending_delete_votes
        ]

        # Filter Votes with user and content_object
        Vote.objects.filter(
            Q(user__in=users) & Q(content_type__in=content_models),
            Q(object_id__in=content_object_ids),
        ).delete()

        # Delete their cache
        cache.delete_many(pending_delete_votes)
