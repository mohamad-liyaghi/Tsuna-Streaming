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

class ChennelAdminPermission(BasePermission):
    '''A permission for controling users access to channel admin list/detail'''
    message = 'Access denied or result is empty'

    def has_permission(self, request, view):

        object = view.get_queryset().first()
        
        if object:

            if request.user == object.channel.owner:
                return True
            
            elif ChannelAdmin.objects.filter(user=request.user, channel=object.channel):
                return True

            return False
        
        return False
    

class ChannelAdminDetailPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.channel.owner or request.user == obj.promoted_by:
            return True
            
        return False