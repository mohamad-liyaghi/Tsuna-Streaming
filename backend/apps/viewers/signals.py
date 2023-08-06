from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from contents.models import AbstractContent
from viewers.tasks import remove_object_viewers
from core.utils import get_content_type_model


@receiver(post_delete, sender=AbstractContent)
def delete_object_viewers_after_deleting(sender, instance, *args, **kwargs):
    """
    Deletes all viewers of an object after deleting it.
    """

    remove_object_viewers.delay(
        content_type_id=get_content_type_model(
            instance.__class__, return_id=True
        ),
        object_id=instance.id,
        object_token=instance.token,
    )
