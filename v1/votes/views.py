from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from votes.serializers import VoteSerializer, VoteListSerializer
from votes.mixins import VoteQuerysetMixin



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

        upvotes = self.votes.upvotes()
        downvotes = self.votes.downvotes()

        return Response({"upvotes" : upvotes, "downvotes" : downvotes, "voted" : True if self.user_vote else False,
        "user_vote" : self.user_vote.choice if self.user_vote else None}, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            # if user hasnt voted yet, an object would be created
            if not self.user_vote:
                serializer.save(user=request.user, content_object=self.object)
                return Response("Vote saved", status=status.HTTP_201_CREATED)

            # if user posted a former vote for 2 times, the former vote will be deleted
            elif serializer.data.get("choice", None) == self.user_vote.choice:
                self.user_vote.delete()
                return Response("Vote deleted.", status=status.HTTP_200_OK)
            
            # if user post diffrent data in comparison to former vote, it will be updated
            elif (choice:=serializer.data.get("choice", None)) != self.user_vote.choice:
                self.user_vote.choice = choice
                self.user_vote.save()
                return Response("Vote saved", status=status.HTTP_200_OK)

        return Response("Invalid information", status=status.HTTP_400_BAD_REQUEST)



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