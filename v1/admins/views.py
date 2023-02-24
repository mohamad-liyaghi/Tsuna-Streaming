from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from admins.models import Admin
from admins.serializers import AdminListSerializer, AdminCreateSerializer
from admins.mixins import AdminPermissionMixin
from channels.models import Channel



@extend_schema_view(
    get=extend_schema(
        description="List of a channels admins."
    ),
    post=extend_schema(
        description="Promote a user to admin."
    ),
)
class AdminListCreateView(AdminPermissionMixin, ListCreateAPIView):
    '''List and Create an Admin for chanenl'''

    permission_classes = [IsAuthenticated,]

    def get_serializer_context(self):
        '''Send context to serializer for creating admin'''
        return {'request_user' : self.request.user, 'channel' : self.channel}

    def get_queryset(self):
        # return admins of a channel.
        return Admin.objects.filter(channel=self.channel)


    def get_serializer_class(self):
        '''Return appropriate serializer for each view'''
        
        if self.request.method == "GET":
            return AdminListSerializer

        return AdminCreateSerializer
