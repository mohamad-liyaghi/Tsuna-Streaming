from viewers.tasks import remove_object_viewers
from core.utils import get_content_type_model


def delete_object_viewers_after_deleting(sender, instance, *args, **kwargs):
    """
    Deletes all viewers of an object after deleting it.
    """

    remove_object_viewers.delay(
        get_content_type_model(
            instance.__class__, return_id=True
        ), instance.id
    )
