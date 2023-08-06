from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from core.utils import get_content_type_by_id
from channels.models import Channel


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


class ContentObjectMixin(ContentTypeModelMixin):
    """
    Retrieve the object that user is trying to access.
    """

    def get_object(self, bypass_permission: bool = False):
        """
        Get the object from the URL
        The self.model is set in the ContentTypeModelMixin
        """

        # Get the object from the URL
        content_object = get_object_or_404(
            self.model,
            token=self.kwargs.get('object_token')
        )

        # Check permissions for the object if bypass_permission is False
        if not bypass_permission:
            # Check permissions for the object
            self.check_object_permissions(self.request, content_object)

        return content_object


class ChannelObjectMixin:
    """
    Get the channel object from the channel token.
    """
    def dispatch(self, request, *args, **kwargs):
        # Set as self.channel
        self.channel = get_object_or_404(
            Channel, token=self.kwargs['channel_token']
        )
        return super().dispatch(request, *args, **kwargs)
