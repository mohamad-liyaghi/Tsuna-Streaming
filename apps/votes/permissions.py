from rest_framework.permissions import BasePermission
from votes.models import Vote


class CanCreateVotePermission(BasePermission):
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


class CanDeleteVotePermission(BasePermission):
    """
    Check if the user can delete vote or not.
    """

    message = "You have not voted to this object."

    def has_object_permission(self, request, view, obj):
        """
        Check if user has voted
        """
        vote_status = bool(
            Vote.objects.get_from_cache(
                channel=obj.channel,
                user=request.user,
                content_object=obj
            )
        )
        return vote_status
