from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from celery import shared_task
from viewers.models import Viewer
from v1.core.models import BaseContentModel
from accounts.models import Account


@shared_task
def insert_viewer_into_db():
    '''Insert viewers from cache into db'''

    # get all viewers from db
    viewer_keys = cache.keys("viewer:*:*")

    if viewer_keys:

        for key in viewer_keys:
            viewer = cache.get(key)
            _, object_token, user_token = key.split(':') # viewer:model-obj:user_token
            
            if (viewer and viewer.get('source', '') == 'cache'):

                try:
                    # the content model (Eg: video)
                    object_model = next(
                        model for model in BaseContentModel.__subclasses__() \
                        if model.__name__.lower() == object_token.split('-')[0]
                    )
                    
                    Viewer.objects.create(                        
                        user = Account.objects.get(token=user_token),
                        content_object = object_model.objects.get(token=object_token),
                        date = viewer.get('date'),
                    )

                    # change viewer status from cache to database
                    viewer['source'] = 'database'
                    cache.set(key, viewer)
            
                except:
                    # if the object were not found
                    cache.delete(key)


@shared_task
def remove_object_viewers(object_model_content_type_id, object_id):
    '''Remove all objects viewers with celery'''

    # get the object model content type (eg: Video)
    model = ContentType.objects.get(id=object_model_content_type_id)

    # delete all related viewers
    Viewer.objects.filter(content_type=model, object_id=object_id).delete()