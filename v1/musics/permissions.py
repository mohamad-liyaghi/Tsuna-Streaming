from rest_framework.permissions import BasePermission
from musics.models import Music


class CreateMusicPermission(BasePermission):
    message = 'You are not allowed to add music to this channel'

    def has_permission(self, request, view):
        """
        Returns True if the user has permission to add music to the channel, False otherwise.
        """
        
        channel = view.channel
        
        if request.method == "POST":
            # Check if user is admin
            if (admin:=channel.admins.filter(user=request.user).first()):
                # If user is admin, check if user has permission to add music
                return (admin and admin.permissions.filter(model=Music.get_model_content_type(), add_object=True))
            
            return False
        
        return True
    