from django.contrib.contenttypes.models import ContentType
from celery import shared_task
from comments.models import Comment


@shared_task
def remove_object_comments(object_model_content_type_id, object_id):
    '''Remove all objects comments with celery'''
    
    # get the object model content type (eg: Video)
    model = ContentType.objects.get(id=object_model_content_type_id)

    # delete all related comments
    Comment.objects.filter(content_type=model, object_id=object_id).delete()