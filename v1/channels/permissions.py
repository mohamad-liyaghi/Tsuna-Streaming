from rest_framework.permissions import BasePermission
from channels.models import ChannelAdmin

class ChannelLimitPermission(BasePermission):
    '''This permission doesnt let users to create channels more than expected amount'''
    
    message = "You have reached the maximum number of channels you have created."
    
    def has_permission(self, request, view):
        user = request.user

        if user.is_authenticated:
            if user.role in ["a", "p"]:
                return not bool(user.channels.count() >= 10)
            
            elif user.role == 'n':
                if user.channels.count() > 5 and user.channels.count() < 10:
                    return True

                elif user.channels.count() < 5:
                    return True
                    
                return False
                
        return False    



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

            return (request.user.admin.filter(channel=object, change_channel_info=True).exists())

        return True
