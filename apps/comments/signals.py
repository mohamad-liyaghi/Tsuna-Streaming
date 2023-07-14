from comments.tasks import remove_object_comments
from core.utils import get_content_type_model


def delete_object_comments_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects comments that has been saved in db.'''

    remove_object_comments.delay(
        get_content_type_model(
            model=instance.__class__,
            return_id=True
        ), instance.id
    )
