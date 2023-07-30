from django.shortcuts import get_object_or_404
from apps.core.mixins import ContentTypeModelMixin


class VoteObjectMixin(ContentTypeModelMixin):
    """
    Retrieve the object that user is trying to vote for.
    """

    def get_object(self):
        """
        Get the object from the URL
        The self.model is set in the ContentTypeModelMixin
        """

        # Get the object from the URL
        content_object = get_object_or_404(
            self.model,
            token=self.kwargs.get('object_token')
        )
        # Check permissions for the object
        self.check_object_permissions(self.request, content_object)
        return content_object
