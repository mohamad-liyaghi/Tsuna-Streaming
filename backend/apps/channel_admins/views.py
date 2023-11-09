from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, extend_schema_view

from channel_admins.models import ChannelAdmin, ChannelAdminPermission
from channel_admins.serializers import (
    AdminListSerializer,
    AdminCreateSerializer,
    AdminDetailSerializer,
)
from channel_admins.mixins import ChannelMixin
from channel_admins.permissions import IsChannelOwner
from core.permissions import IsChannelAdmin


@extend_schema_view(
    get=extend_schema(
        description="List of a channels admins [Available for admins].",
        responses={200: "ok", 401: "Unauthorized", 403: "Forbidden"},
        tags=["Channel Admins"],
    ),
    post=extend_schema(
        description="Promote a user to admin [Only by owner].",
        responses={
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
        },
        tags=["Channel Admins"],
    ),
)
class AdminListCreateView(ChannelMixin, ListCreateAPIView):
    """
    List of admins and create a new one.
    Create a New Admin
    Methods: POST, GET
    """

    lookup_url_kwarg = "channel_token"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsChannelAdmin()]
        return [IsAuthenticated(), IsChannelAdmin(), IsChannelOwner()]

    def get_serializer_context(self):
        """
        Pass user/channel to serializer.
        """
        return {"request_user": self.request.user, "channel": self.channel}

    def get_queryset(self):
        channel = self.channel
        return channel.admins.all()

    def get_serializer_class(self):
        """
        Choose the serializer class based on request method.
        """
        if self.request.method == "GET":
            return AdminListSerializer
        return AdminCreateSerializer


@extend_schema_view(
    get=extend_schema(
        description="Retrieve an admins permissions.",
        responses={200: "ok", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},
        tags=["Channel Admins"],
    ),
    put=extend_schema(
        description="Update an admins permissions.",
        responses={
            200: "ok",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
        tags=["Channel Admins"],
    ),
    patch=extend_schema(
        description="Update an admins permissions.",
        responses={
            200: "ok",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
        tags=["Channel Admins"],
    ),
    delete=extend_schema(
        description="Delete an admin.",
        responses={
            204: "No Content",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
        tags=["Channel Admins"],
    ),
)
class AdminDetailView(ChannelMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = AdminDetailSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            # All admins can retrieve the admin
            return [IsAuthenticated(), IsChannelAdmin()]
        # But only owner can update/delete them
        return [IsAuthenticated(), IsChannelAdmin(), IsChannelOwner()]

    def get_object(self):
        return get_object_or_404(
            ChannelAdmin.objects.prefetch_related("permissions"),
            channel__token=self.channel.token,
            token=self.kwargs["admin_token"],
        )

    def get_serializer_context(self):
        """
        Return user and channel to backend
        """
        return {"request_user": self.request.user, "channel": self.channel}

    def destroy(self, request, *args, **kwargs):
        """
        Delete an admin
        Also ensure that user is not deleting himself
        """
        admin = self.get_object()
        if request.user == admin.user:
            return Response(
                {"detail": "You cannot delete yourself."},
                status=status.HTTP_403_FORBIDDEN,
            )
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
