from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import  status


class VoteQuerysetMixin:
    '''Return content type and the object'''

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, object_token, *args, **kwargs):
        token = object_token.split('-') # ['mode', 'token']

        if not len(token) == 2:
            return JsonResponse({"error" : "invalid url format"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.content_model = get_object_or_404(ContentType, model=token[0])

        # get the object
        self.object = get_object_or_404(self.content_model.model_class(), token=object_token)
    
        return super().dispatch(request, *args, **kwargs)