from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from votes.models import Vote


@extend_schema_view(
    get=extend_schema(
        description="Number of upvotes, downvotes, user voted [Boolean], user choice [if voted]."
    ),
)
class RateView(APIView):
    permission_classes = [IsAuthenticated,]

    def dispatch(self, request, content_type_id, token, *args, **kwargs):
        # get the content type model [eg: Video model]
        self.content_type_model = get_object_or_404(ContentType, id=content_type_id)

        # get the object
        self.object = get_object_or_404(self.content_type_model.model_class(), token=token)

        # get all votes related to the object
        self.vote = Vote.objects.filter(content_type=self.content_type_model,
                                             object_id=self.object.id)

        # check if user has voted this object or not
        self.user_vote = self.vote.filter(user=request.user).first()

        return super().dispatch(request, content_type_id, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # TODO add manager to get upvote and downvote 
        upvotes = self.vote.filter(choice="u").count()
        downvotes = self.vote.filter(choice="d").count()

        return Response({"upvotes" : upvotes, "downvotes" : downvotes, "voted" : True if self.user_vote else False,
        "user_vote" : self.user_vote.choice if self.user_vote else None}, status=status.HTTP_200_OK)
