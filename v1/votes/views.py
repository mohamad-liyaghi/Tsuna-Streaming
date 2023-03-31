from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from votes.serializers import VoteSerializer, VoteListSerializer
from votes.mixins import VoteQuerysetMixin
from votes.models import Vote



@extend_schema_view(
    get=extend_schema(
        description="Number of upvotes, downvotes, user voted [Boolean], user choice [if voted]."
    ),
    post=extend_schema(
        description="Vote or delete or update a vote."
    ),
)
class VoteView(VoteQuerysetMixin, APIView):
    '''
        Get: show the upvote and downvotes and also user vote status
        Post: Vote a model
    '''
    permission_classes = [IsAuthenticated,]
    serializer_class = VoteSerializer


    def get(self, request, *args, **kwargs):
        # users votes.
        user_vote = Vote.objects.get_from_cache(self.object, request.user)
        return Response(
            {
                "voted" : True if user_vote else False,
                "user_vote" : user_vote.get('choice', None) if user_vote else None,
                "status" : self.object.get_votes_count(),
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
                    "voted" : True if vote else False,
                    "user_vote" : vote.get('choice', None) if vote else None
                }, 
                status=status.HTTP_201_CREATED)
            
            return Response(vote, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        description="List of users that voted an object."
    ),
)
class VoteListView(VoteQuerysetMixin, APIView):
    '''List of users that voted an object'''

    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        '''Get self.vote from the mixin and pass it to serializer'''

        # self.vote is in mixin
        serializer = VoteListSerializer(self.votes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)