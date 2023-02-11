import uuid

def unique_token_generator(instance):
    '''Creates a unique token for each instance'''

    # the actual model class
    klass =  instance.__class__

    # a 32 char uuid token
    token = token = uuid.uuid4().hex

    if klass.objects.filter(token=token).exists():
        unique_token_generator(instance)
    
    return token
    
    