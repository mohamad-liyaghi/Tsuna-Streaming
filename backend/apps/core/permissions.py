from rest_framework.permissions import BasePermission
from channel_admins.models import ChannelAdmin


class IsChannelAdmin(BasePermission):
    """
    Check if user is an admin of the channel.
    """

    message = 'You are not admin of the channel'

    def has_permission(self, request, view):
        """
        Check if user is an admin of the channel.
        """
        channel = view.channel
        return ChannelAdmin.objects.filter(
            channel=channel, user=request.user
        ).exists()
