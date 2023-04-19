from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from channel_admins.models import ChannelAdmin, ChannelAdminPermission
from channel_admins.serializers import (
    AdminListSerializer,
    AdminCreateSerializer,
    AdminDetailSerializer,
    AdminPermissionDetailSerializer
)
from channel_admins.mixins import AdminPermissionMixin
from channel_admins.permissions import AdminDetailPermission, AdminPermissionUpdate


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
        return ChannelAdmin.objects.filter(channel=self.channel)


    def get_serializer_class(self):
        '''Return appropriate serializer for each view'''
        
        if self.request.method == "GET":
            return AdminListSerializer

        return AdminCreateSerializer


@extend_schema_view(
    get=extend_schema(
        description="Detail page of an admin."
    ),
    put=extend_schema(
        description="Update an admins general permissions."
    ),
    patch=extend_schema(
        description="Update an admins general permissions."
    ),
    delete=extend_schema(
        description="Delete an admin."
    ),
)
class AdminDetailView(AdminPermissionMixin, RetrieveUpdateDestroyAPIView):

    serializer_class = AdminDetailSerializer
    permission_classes = [IsAuthenticated, AdminDetailPermission]

    def get_object(self):
        return get_object_or_404(
                    self.channel.admins.prefetch_related('permissions').all(),
                    token=self.kwargs['admin_token']
            )

    def get_serializer_context(self):
        '''Send context to serializer for creating admin'''
        return {'request_user' : self.request.user, 'channel' : self.channel}
    


@extend_schema_view(
    get=extend_schema(
        description="Admin permission detail page."
    ),
    put=extend_schema(
        description="Update an admins permissions."
    ),
    patch=extend_schema(
        description="Update an admins permissions."
    ),
)
class AdminPermissionDetail(AdminPermissionMixin, RetrieveUpdateAPIView):
    '''A page for controling admins permissions.'''

    serializer_class = AdminPermissionDetailSerializer
    permission_classes = [IsAuthenticated, AdminPermissionUpdate]

    def get_object(self):
        admin = get_object_or_404(ChannelAdmin, token=self.kwargs['admin_token'], channel=self.channel)
        return get_object_or_404(ChannelAdminPermission.objects.select_related('admin'), admin=admin, token=self.kwargs['permission_token'])
    
    