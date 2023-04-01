from django.http import JsonResponse, Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import status
from v1.core.models import BaseContentModel

class ContentModelMixin:
    '''Return content type and the object'''

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):

        # Get the object token from the URL.
        self.object_token = self.kwargs.get('object_token')

        # Split the token into "model" and "token" parts.
        model_name, token = self.object_token.split('-')

        if not (model_name and token):
            return JsonResponse({'error': 'invalid object token format'}, status=status.HTTP_400_BAD_REQUEST)

        # Look up the content model by name.
        try:
            # check if given content model is subclass of BaseContentModel
            self.content_model = next(
                subclass for subclass in BaseContentModel.__subclasses__() if subclass.__name__.lower() == model_name
                )

        except StopIteration:
            raise Http404('Content model does not exist.')

        return super().dispatch(request, *args, **kwargs)
