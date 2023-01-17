from django.contrib.contenttypes.models import ContentType
import uuid

def channel_token_generator():
    '''Create a unique token for each channel'''
    
    token = uuid.uuid4().hex
    Channel = ContentType.objects.get(app_label="channels", model="channel").model_class()

    if Channel.objects.filter(token=token):
        channel_token_generator()

    return token