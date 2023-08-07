from celery import shared_task
from comments.models import Comment
from core.utils import get_content_type_model


@shared_task
def remove_object_comments(content_type_id: int, object_id: int):
    """
    Remove all comments related to an object after its deletion.
    """
    # get the object model content type (eg: Video)
    content_model = get_content_type_model(_id=content_type_id).id
    # Delete Related Comments
    Comment.objects.filter(
        content_type=content_model, object_id=object_id
    ).delete()
