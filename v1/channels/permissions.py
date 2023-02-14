from django.shortcuts import get_object_or_404
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


class ChannelAdminDetailPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.channel.owner or request.user == obj.promoted_by)


class ChannelPermission(BasePermission):
    '''Channel Permissions'''
    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        
        object = view.get_object()
        
        # check permission for deleting channel
        if request.method == "DELETE":
            if request.user == object.owner:
                return True

            return False

        # check permission for updating channel
        elif request.method in ["PUT", "PATCH"]:

            if request.user == object.owner or \
                ChannelAdmin.objects.filter(user=request.user, channel=object, change_channel_info=True).exists():
                return True

            return False
        
        return True
