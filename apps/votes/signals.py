from votes.tasks import remove_object_votes
from core.utils import get_content_type_model



def delete_object_votes_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects votes that has been saved in db.'''

    # use celery to delete object votes
    remove_object_votes.delay(
        get_content_type_model(
            instance.__class__, return_id=True
        ),
        instance.id
    )
