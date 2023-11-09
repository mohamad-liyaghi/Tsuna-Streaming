from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from votes.serializers import (
    VoteStatusSerializer,
    VoteListSerializer,
    VoteCreateSerializer,
)
from votes.models import Vote, VoteChoice
from votes.permissions import CanCreateVotePermission, CanDeleteVotePermission
from core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(
        description="Check if a user has votes to an object or not.",
        responses={
            200: "ok",
            401: "Unauthorized",
            404: "Not found",
        },
        tags=["Votes"],
    ),
)
class VoteStatusView(ContentObjectMixin, APIView):
    """
    Return users vote if voted;
    Else return None.
    """

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = VoteStatusSerializer

    def get(self, request, *args, **kwargs):
        # Self.object is set in ContentObjectMixin
        content_object = self.get_object()

        # Get the vote from cache and db
        vote_status = Vote.objects.get_from_cache(
            channel=content_object.channel,
            user=request.user,
            content_object=content_object,
        )
        if vote_status:
            return Response(
                VoteStatusSerializer(instance=vote_status).data,
                status=status.HTTP_200_OK,
            )

        # Return None if user hasnt voted.
        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        description="Create a vote for an object.",
        responses={
            201: "Created",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Votes"],
    ),
)
class VoteCreateView(ContentObjectMixin, CreateAPIView):
    """
    Create a vote for an object.
    """

    permission_classes = [IsAuthenticated, CanCreateVotePermission]
    serializer_class = VoteCreateSerializer

    def get_serializer_context(self):
        return {"content_object": self.get_object, "user": self.request.user}


@extend_schema_view(
    delete=extend_schema(
        description="Delete a vote for an object.",
        responses={
            204: "No content",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Votes"],
    ),
)
class VoteDeleteView(ContentObjectMixin, DestroyAPIView):
    """
    Delete a vote for an object.
    """

    permission_classes = [IsAuthenticated, CanDeleteVotePermission]

    def destroy(self, request, *args, **kwargs):
        # Self.object is set in ContentObjectMixin
        content_object = self.get_object()
        # Delete the vote
        Vote.objects.delete_in_cache(
            channel=content_object.channel,
            user=request.user,
            content_object=content_object,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        description="List of users that voted an object.",
        responses={
            200: "ok",
            401: "Unauthorized",
            404: "Not found",
        },
        tags=["Votes"],
    ),
)
class VoteListView(ContentObjectMixin, ListAPIView):
    """
    List of users that voted for an object.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = VoteListSerializer

    def get_queryset(self):
        content_object = self.get_object()

        return Vote.objects.get_list(
            channel=content_object.channel, content_object=content_object
        )
