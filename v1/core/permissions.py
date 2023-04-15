from rest_framework.permissions import BasePermission

class IsChannelAdmin(BasePermission):
    '''Check if user is the channels admin'''

    message = 'You are not admin of the channel'
    
    def has_permission(self, request, view):
        return (view.object.channel.admins.filter(user=request.user))