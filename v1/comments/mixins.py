from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

class CommentObjectMixin():
    '''Get the content type model and the passed object.'''
    def dispatch(self, request, *args, **kwargs):
        content_type_id = self.kwargs.get("content_type_id")
        object_token = self.kwargs.get('object_token')

        # get the content type model [eg: Video model]
        self.content_type_model = get_object_or_404(ContentType, id=content_type_id)

        # get the object
        self.object = get_object_or_404(self.content_type_model.model_class(), token=object_token)
        return super().dispatch(request, *args, **kwargs)