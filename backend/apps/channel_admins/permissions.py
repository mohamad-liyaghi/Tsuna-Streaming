from rest_framework.permissions import BasePermission


class IsChannelOwner(BasePermission):
    """
    Check if user is the channel owner
    """

    message = 'You are not the owner of the channel.'

    def has_permission(self, request, view):
        """
        Check if the user is the owner of the channel.
        The view.channel is provided by the `ChannelMixin` for the view
        """
        return request.user == view.channel.owner
