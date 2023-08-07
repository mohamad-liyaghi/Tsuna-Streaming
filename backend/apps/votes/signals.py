from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from contents.models import AbstractContent
from votes.tasks import remove_object_votes
from core.utils import get_content_type_model


@receiver(post_delete, sender=AbstractContent)
def delete_vote_after_deleting_object(sender, instance, *args, **kwargs):
    """
    When an object is deleted,
    all the votes related to that object will be deleted too.
    """

    # Call the celery task to delete them
    remove_object_votes.delay(
        content_type_id=get_content_type_model(model=type(instance)).id,
        object_id=instance.id,
        object_token=instance.token
    )
