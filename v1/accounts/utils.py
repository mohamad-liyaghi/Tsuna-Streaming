from django.contrib.contenttypes.models import ContentType
import uuid, random

def token_generator():
    return uuid.uuid4().hex
