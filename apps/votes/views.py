from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from votes.serializers import VoteStatusSerializer, VoteListSerializer, VoteCreateSerializer
from votes.models import Vote, VoteChoice
from votes.permissions import CanCreateVotePermission, CanDeleteVotePermission
from votes.mixins import VoteObjectMixin
from core.permissions import IsChannelAdmin
from apps.core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(
        description="Check if a user has votes to an object or not.",
        responses={
            200: 'ok',
            401: "Unauthorized",
            404: "Not found",
        },
        tags=['Votes']
    ),
)
class VoteStatusView(VoteObjectMixin, APIView):
    """
    Return Vote status of a user
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = VoteStatusSerializer

    def get(self, request, *args, **kwargs):
        # Self.object is set in VoteObjectMixin
        content_object = self.get_object()

        # Check if user has voted or not
        vote_status = Vote.objects.get_from_cache(
                channel=content_object.channel,
                user=request.user,
                content_object=content_object
            )
        if vote_status:
            serialized_data = VoteStatusSerializer(instance=vote_status)

            return Response(
                serialized_data.data, status=status.HTTP_200_OK
            )

        return Response(
            status=status.HTTP_200_OK
        )


@extend_schema_view(
    post=extend_schema(
        description="Create a vote for an object.",
        responses={
            201: 'Created',
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=['Votes']
    ),
)
class VoteCreateView(VoteObjectMixin, CreateAPIView):
    """
    Create a vote for an object.
    """
    permission_classes = [IsAuthenticated, CanCreateVotePermission]
    serializer_class = VoteCreateSerializer

    def get_serializer_context(self):
        return {
            'content_object': self.get_object,
            'user': self.request.user
        }


@extend_schema_view(
    delete=extend_schema(
        description="Delete a vote for an object.",
        responses={
            204: 'No content',
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=['Votes']
    ),
)
class VoteDeleteView(VoteObjectMixin, DestroyAPIView):
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
        description="List of users that voted an object."
    ),
)
class VoteListView(ContentObjectMixin, APIView):
    """
    List of users that voted for an object.
    """

    permission_classes = [IsAuthenticated, IsChannelAdmin]

    def get(self, request, *args, **kwargs):
        """
        Get list of people who have voted from the database and cache.
        """

        # Create a dict from all users who has voted in cache
        votes_in_cache = [
            {
            "user": key.split(":")[2], 
            "choice": cache.get(key)["choice"],
            }
            for key in cache.keys(f"vote:{self.object.token}:*")
            if cache.get(key)['source'] == 'cache' 
        ]

        # Get votes that are in db [from cache]
        votes_in_db = cache.get(f'db_vote:{self.object.token}')

        if votes_in_db is None:
                
                # Get all votes from database
                database_vote = [
                    (db_vote.user.token, db_vote.choice)
                    for db_vote in list(self.object.votes.select_related('user').all())
                ]

                # Check if they are not saved in cache
                votes_in_db = [
                    {"user": user_token, "choice": choice}
                    for user_token, choice in database_vote
                    if not any(vote["user"] == user_token for vote in votes_in_cache)
                ]

                # Set in cache            
                cache.set(key=f'db_vote:{self.object.token}', value=votes_in_db, timeout=5)

        # all votes
        votes = []
        votes += votes_in_cache + votes_in_db

        serializer = VoteListSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)