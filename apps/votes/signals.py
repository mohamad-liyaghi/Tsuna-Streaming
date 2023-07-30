from votes.tasks import remove_object_votes
from core.utils import get_content_type_model


def delete_vote_after_deleting_object(sender, instance, *args, **kwargs):
    """
    When an object is deleted,
    all the votes related to that object will be deleted too.
    """

    # Call the celery task to delete them
    remove_object_votes.delay(
        get_content_type_model(
            instance.__class__, return_id=True
        ),
        instance.id
    )
