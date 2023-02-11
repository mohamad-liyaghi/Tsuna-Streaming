from django.contrib.contenttypes.models import ContentType
import uuid, random

def token_generator():
    return uuid.uuid4().hex

def user_id_generator():
    '''Create a unique user id for accounts'''
    # get the accounts model 
    Account = ContentType.objects.get(app_label='accounts', model="account").model_class()
    
    user_id = random.randint(0, 999999999999999)

    # if user with generated userid exists, function get calls again.
    if Account.objects.filter(token=user_id):
        user_id_generator()

    return user_id