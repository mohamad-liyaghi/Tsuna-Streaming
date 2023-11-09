from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from comments.tasks import remove_object_comments
from core.utils import get_content_type_model


@receiver(post_delete, sender=AbstractContent)
def delete_object_comments_after_deleting(sender, instance, *args, **kwargs):
    """
    Delete object comments after deleting the object.
    """
    remove_object_comments.delay(
        content_type_id=get_content_type_model(model=type(instance)),
        object_id=instance.id,
    )
