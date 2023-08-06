from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from contents.permissions import (
    CreateContentPermission,
    DeleteContentPermission,
    UpdateContentPermission,
    RetrievePrivateContentPermission
)
from viewers.decorators import ensure_viewer_exists
from core.mixins import ChannelObjectMixin
from core.permissions import IsChannelAdmin
from contents.models import ContentVisibility


class ContentListCreateView(ChannelObjectMixin, ListCreateAPIView):
    """
    Core View for Listing/Creating a content (video or music)
    """

    filterset_fields = ['title']
    model = None

    def get_permissions(self):
        """
        Return required permissions based on method.
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsChannelAdmin(), CreateContentPermission()]

        if self.request.GET.get('show_private', False):
            return [IsAuthenticated(), IsChannelAdmin()]

        return [IsAuthenticated(), ]

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {'user': self.request.user, 'channel': self.channel}

    def get_queryset(self):
        """
        List of a channels contents
        """
        queryset = self.model.objects.select_related('user', 'channel') \
            .filter(channel=self.channel).order_by("-date")

        if self.request.GET.get('show_private', False):
            return queryset

        return queryset.filter(visibility=ContentVisibility.PUBLISHED)


class ContentDetailView(ChannelObjectMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "token"
    model = None

    def get_permissions(self):
        """
        Return appropriate permissions based on request method.
        """
        match self.request.method:
            case "DELETE":
                return [IsAuthenticated(), IsChannelAdmin(), DeleteContentPermission()]
            case "PUT" | "PATCH":
                return [IsAuthenticated(), IsChannelAdmin(), UpdateContentPermission()]
            case _:
                return [IsAuthenticated(), RetrievePrivateContentPermission()]

    def get_object(self):
        """
        Get the content and check its permissions
        """
        content = get_object_or_404(
            self.model.objects.select_related("channel", "user"),
            token=self.kwargs["object_token"],
            channel=self.channel
        )
        self.check_object_permissions(self.request, content)
        return content

    @ensure_viewer_exists
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
