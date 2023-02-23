from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView

from drf_spectacular.utils import extend_schema, extend_schema_view

from admins.models import Admin
from admins.serializers import AdminListSerializer
from channels.models import Channel

@extend_schema_view(
    get=extend_schema(
        description="List of a channels admins."
    ),
)
class AdminListCreateView(ListCreateAPIView):
    '''List and Create an Admin for chanenl'''

    def get_queryset(self):
        # return admins of a channel.
        return Admin.objects.filter(channel__token=self.kwargs['channel_token'])


    def get_serializer_class(self):
        '''Return appropriate serializer for each view'''
        if self.request.method == "GET":
            return AdminListSerializer

        return AdminListSerializer
