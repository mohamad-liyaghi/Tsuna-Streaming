from rest_framework.permissions import BasePermission
from votes.models import Vote


class CanVotePermission(BasePermission):
    """
    Check if the user can vote or not.
    """

    message = "You have already voted to this object."

    def has_object_permission(self, request, view, obj):
        """
        Check if user has not voted yet
        """
        vote_status = bool(
            Vote.objects.get_from_cache(
                channel=obj.channel,
                user=request.user,
                content_object=obj
            )
        )
        return not vote_status
