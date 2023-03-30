from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType


class VoteQuerysetMixin:
    '''Return content type and the object'''

    def dispatch(self, request, object_token, *args, **kwargs):
        token = object_token.split('-') # ['mode', 'token']

        if not len(token) == 2:
            raise ValueError("NIOO")
        
        self.content_model = get_object_or_404(ContentType, model=token[0])

        # get the object
        self.object = get_object_or_404(self.content_model.model_class(), token=object_token)
    
        return super().dispatch(request, *args, **kwargs)