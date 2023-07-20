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
            # TODO: update this with build in permission
            return (
                request.user.channel_admins.filter(channel=obj, change_channel_info=True).exists()
            )
        # If request is GET
        return True
