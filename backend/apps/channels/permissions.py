from rest_framework.permissions import BasePermission


class IsChannelStaff(BasePermission):
    """
        A permission for channel Viewset
        Delete -> Only channel owner can delete the channel.
        Update -> Only admins with change_channel_info permission can update the channel.
    """

    message = "Only channel admins can perform this action."

    def has_object_permission(self, request, view, obj):

        # Only channel owner can delete the channel.
        if request.method == "DELETE":
            return request.user == obj.owner

        # check permission for updating channel
        elif request.method in ["PUT", "PATCH"]:

            # Get the admin object
            channel_admin = request.user.channel_admins.filter(channel=obj).first()
            # Check if admin has permission to change channel info
            return channel_admin and channel_admin.permissions.can_change_channel_info

        # If request is GET
        return True
