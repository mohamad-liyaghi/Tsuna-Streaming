from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from admins.models import Admin
from admins.serializers import AdminListSerializer, AdminCreateSerializer, AdminDetailSerializer
from admins.mixins import AdminPermissionMixin, UpdateAdminMixin



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



@extend_schema_view(
    get=extend_schema(
        description="Detail page of an admin."
    ),
)
class AdminDetailView(AdminPermissionMixin, UpdateAdminMixin, RetrieveUpdateDestroyAPIView):

    serializer_class = AdminDetailSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return get_object_or_404(
                    self.channel.admins.prefetch_related('permissions').all(),
                    token=self.kwargs['admin_token']
            )

    def get_serializer_context(self):
        '''Send context to serializer for creating admin'''
        return {'request_user' : self.request.user, 'channel' : self.channel}