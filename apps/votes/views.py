from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from votes.serializers import VoteSerializer, VoteListSerializer
from apps.core.mixins import ContentObjectMixin
from votes.models import Vote
from core.permissions import IsChannelAdmin

@extend_schema_view(
    get=extend_schema(
        description="Number of upvotes, downvotes, user voted [Boolean], user choice [if voted]."
    ),
    post=extend_schema(
        description="Vote or delete or update a vote."
    ),
)
class VoteView(ContentObjectMixin, APIView):
    '''
        Get: show the upvote and downvotes and also user vote status
        Post: Vote a model
    '''
    permission_classes = [IsAuthenticated, ]
    serializer_class = VoteSerializer

    def get(self, request, *args, **kwargs):

        # users votes.
        user_vote = Vote.objects.get_from_cache(self.object, request.user)

        return Response(
            {
                "voted": True if user_vote else False,
                "user_vote": user_vote.get('choice', None) if user_vote else None,
                # "status": self.object.get_votes_count(), TODO: make this work
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            vote = Vote.objects.create_in_cache(
                user=request.user,
                content_object=self.object,
                choice=serializer.validated_data['choice']
            )
            if vote:
                return Response(
                    {
                        "voted": True if vote else False,
                        "user_vote": vote.get('choice', None) if vote else None
                    },
                    status=status.HTTP_201_CREATED)

            return Response(vote, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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