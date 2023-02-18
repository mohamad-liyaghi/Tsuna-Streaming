from v1.core.utils import unique_token_generator


def create_token_after_creating_object(sender, instance, *args, **kwargs):
    '''Set a default token for each generated object'''
    
    # get and process a new token for object (check if it does not exist)
    token = unique_token_generator(instance)
    
    if not instance.pk:
        instance.token = token
