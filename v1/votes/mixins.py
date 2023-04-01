from django.shortcuts import get_object_or_404
from v1.core.mixins import ContentModelMixin


class VoteQuerysetMixin(ContentModelMixin):
    '''Return content type and the object'''

    def get_object(self):
        return get_object_or_404(self.content_model, token=self.object_token)
