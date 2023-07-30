from django.core.cache import cache
from celery import shared_task
from votes.models import Vote
from accounts.models import Account
from apps.core.models import AbstractContent
from core.utils import get_content_type_model


@shared_task
def remove_object_votes(content_type_id: int, object_id: int):
    """
    Remove all objects votes
    """
    # get the object model content type (eg: Video)
    model = get_content_type_model(content_type_id)
    # delete all related votes
    Vote.objects.filter(content_type=model, object_id=object_id).delete()


# TODO: update this
@shared_task
def insert_vote_into_db():
    # get votes from db
    vote_keys = cache.keys("vote:*:*")

    if vote_keys:
        for key in vote_keys:

            vote = cache.get(key)
            _, object_token, user_token = key.split(':') # vote:model-obj:user_token
            
            if (vote and vote.get('source', '') == 'cache' or \
                vote and vote.get('source', '') == 'database' and vote.get('deleted', '') == True):

                object_model = AbstractContent.get_content_model_by_name((object_token.split('-')[0]).capitalize())

                if object_model:

                    try:
                        # Object to vote
                        object = object_model.objects.get(token=object_token)

                        # if vote is getting created twice, it will be deleted in process
                        # otherwise create a vote
                        db_vote = Vote.objects.create(                        
                            user = Account.objects.get(token=user_token),
                            content_object = object,
                            choice = vote.get('choice')
                        )
                        # change vote status from cache to database
                        if db_vote:
                            vote['source'] = 'database'
                            cache.set(key, vote)
                        else:
                            cache.delete(key)
                

                    except:
                        cache.delete(key)

                else:
                    # if content model does not exist
                    cache.delete(key)