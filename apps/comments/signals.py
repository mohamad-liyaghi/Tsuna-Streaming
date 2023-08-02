from comments.tasks import remove_object_comments
from core.utils import get_content_type_model


def delete_object_comments_after_deleting(sender, instance, *args, **kwargs):
    """
    Delete object comments after deleting the object.
    """
    remove_object_comments.delay(
        content_type_id=get_content_type_model(
            model=instance.__class__,
            return_id=True
        ),
        object_id=instance.id
    )
