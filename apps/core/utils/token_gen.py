import uuid


# TODO: remove this
def unique_token_generator(instance, BaseContentModel):
    '''Creates a unique token for each instance'''

    # the actual model class
    klass =  instance.__class__

    # a 32 char uuid token
    token = uuid.uuid4().hex

    # If the class inherits from content model (e.g. video), 
    # the model name will come first in the token due to the vote and comment functionalities.
    if BaseContentModel.get_content_model_by_name(klass.__name__):
        token = f'{klass.__name__.lower()}-{token [len(klass.__name__.lower()) + 1:]}' # eg: 'video-27b0f...'

    if klass.objects.filter(token=token).exists():
        unique_token_generator(instance)
    
    return token
    
    