from rest_framework.permissions import BasePermission


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
    def has_object_permission(self, request, view, obj):
        #TODO check channel admin list
        return bool(request.user == obj.owner)