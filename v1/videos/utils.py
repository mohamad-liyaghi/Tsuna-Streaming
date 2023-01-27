from django.contrib.contenttypes.models import ContentType
import uuid


def video_token_generator():
    '''Create a unique token for each viedo'''
    
    token = uuid.uuid4().hex
    Video = ContentType.objects.get(app_label="videos", model="video").model_class()
    
    if Video.objects.filter(token=token):
        video_token_generator()

    return token