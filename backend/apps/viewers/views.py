from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from drf_spectacular.utils import extend_schema, extend_schema_view

from viewers.serializers import ViewerListSerializer
from viewers.models import Viewer
from core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(
        description="List of an objects viewers.",
        responses={
            200: "ok",
            401: "Unauthorized",
            404: "Not found",
        },
        tags=["Viewers"],
    ),
)
class ViewerListView(ContentObjectMixin, ListAPIView):
    """
    Return a list of viewers for an object.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ViewerListSerializer

    def get_queryset(self):
        content_object = self.get_object()
        # Get the viewers from cache and db and return
        return Viewer.objects.get_list(
            channel=content_object.channel, content_object=content_object
        )
