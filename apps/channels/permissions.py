from rest_framework.permissions import BasePermission

class ChannelPermission(BasePermission):
    '''
        A permission for channel Viewset
        Delete -> Only channel owner can delete the channel.
        Update -> Only admins with change_channel_info permission can update the channel.
    '''

    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        
        object = view.get_object()
        
        # check permission for deleting channel
        if request.method == "DELETE":
            return (request.user == object.owner)

        # check permission for updating channel
        elif request.method in ["PUT", "PATCH"]:

            return (request.user.channel_admins.filter(channel=object, change_channel_info=True).exists())

        return True
