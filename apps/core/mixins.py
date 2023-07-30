from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status
from apps.core.models import AbstractContent
from core.utils import get_content_type_by_id


# TODO: remove this
class ContentObjectMixin:
    '''Return content type and the object'''

    def dispatch(self, request, *args, **kwargs):

        # Get the object token from the URL.
        object_token = self.get('object_token')

        # Split the token into "model" and "token" parts.
        model_name, token = object_token.split('-')

        if not (model_name and token):
            return JsonResponse(
                {'error': 'invalid object token format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the content model from cache
        content_model = cache.get(f"content_model:{model_name}")

        # Look up the content model by name if not exist in cache.
        if not content_model:
            # check if given content model is subclass of AbstractContent
            content_model = AbstractContent.get_content_model_by_name(
                model_name.capitalize()
            )

            if content_model:
                # set the model in cache
                cache.set(
                    key=f'content_model:{model_name}', value=content_model
                )

            else:
                raise Http404('Content model does not exist.')

        # The object given by URL
        self.object = get_object_or_404(content_model, token=object_token)

        return super().dispatch(request, *args, **kwargs)


class ContentTypeModelMixin:
    """
    Return the content type model for the given content type id
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Get the content type model and set to self.model
        for the given content type id in the url kwargs
        """

        # Get the object token from the URL.
        content_type_id = kwargs.get('content_type_id', None)
        content_type = get_content_type_by_id(_id=content_type_id)

        if not content_type:
            return JsonResponse(
                {'error': 'Content type model not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Set the content type model to self.model
        self.model = content_type.model_class()
        return super().dispatch(request, *args, **kwargs)
