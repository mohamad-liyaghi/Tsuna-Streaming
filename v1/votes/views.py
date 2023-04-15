from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from votes.serializers import VoteSerializer, VoteListSerializer
from v1.core.mixins import ContentObjectMixin
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
                "status": self.object.get_votes_count(),
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            vote = Vote.objects.create_in_cache(
                user=request.user,
                object=self.object,
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

    @method_decorator(cache_page(60 * 2))
    def get(self, request, *args, **kwargs):
        """
        Get list of people who have voted from the database and cache.
        """

        pattern = f"vote:{self.object.token}:*"

        # get all votes keys
        keys = cache.keys(pattern)

        # Extract user and choice values for each key and create a list of dictionaries.
        votes_in_cache = [
            {"user": key.split(":")[2], "choice": cache.get(key)["choice"]} for key in keys
        ]

        # get all the votes in db
        votes_in_db = list(self.object.votes.all())

        votes = []
        votes += votes_in_cache

        # get token of users that voted in cache
        cache_votes_user_tokens = set(vote["user"] for vote in votes_in_cache)

        # if cache in db, does not exist in db, append it to votes list
        for db_vote in votes_in_db:
            if db_vote.user.token not in cache_votes_user_tokens:
                votes.append({'user': db_vote.user.token, 'choice': db_vote.choice})


        serializer = VoteListSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)