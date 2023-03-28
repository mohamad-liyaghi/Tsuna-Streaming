from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class VoteQuerysetMixin:
    '''Return content type and the object'''

    @method_decorator(cache_page(60))
    def dispatch(self, request, content_type_id, object_token, *args, **kwargs):
        # get the content type model [eg: Video model]

        self.content_type_model = get_object_or_404(ContentType, id=content_type_id)

        # get the object
        self.object = get_object_or_404(self.content_type_model.model_class(), token=object_token)

        # get all votes related to the object
        self.votes = self.object.votes.all()

        # users votes.
        self.user_vote = self.votes.filter(user=request.user).first()
    
        return super().dispatch(request, *args, **kwargs)