from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status
from v1.core.models import BaseContentModel


class ContentObjectMixin:
    '''Return content type and the object'''

    def dispatch(self, request, *args, **kwargs):

        # Get the object token from the URL.
        object_token = self.kwargs.get('object_token')

        # Split the token into "model" and "token" parts.
        model_name, token = object_token.split('-')

        if not (model_name and token):
            return JsonResponse({'error': 'invalid object token format'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get the content model from cache
        content_model = cache.get(f"content_model:{model_name}")

        # Look up the content model by name if not exist in cache.
        if not content_model:
            try:
                # check if given content model is subclass of BaseContentModel
                content_model = next(
                    subclass for subclass in BaseContentModel.__subclasses__() if subclass.__name__.lower() == model_name
                    )
                
                # set the model in cache
                cache.set(key=f'content_model:{model_name}', value=content_model)
                
            except StopIteration:
                raise Http404('Content model does not exist.')
            
        # The object given by URL
        self.object = get_object_or_404(content_model, token=object_token)

        return super().dispatch(request, *args, **kwargs)
