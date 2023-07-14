from rest_framework.permissions import BasePermission
from core.utils import get_content_type_model
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
                return (admin and admin.permissions.filter(model=get_content_type_model(Music), add_object=True))
            
            return False
        
        return True
    


class MusicDetailPermission(BasePermission):
    message = 'Permission denied.'
    
    def has_permission(self, request, view):

        if request.method == "GET":
            return True
        
        admin = request.user.channel_admins.filter(channel=view.channel).first()

        # only channel owner and some admins can update a music
        if request.method in ["PUT", "PATCH"]:
            return (admin and admin.permissions.filter(model=get_content_type_model(Music, return_id=True), edit_object=True))


        # only channel owner and some admins can delete a music
        elif request.method == "DELETE":
            return (admin and admin.permissions.filter(model=get_content_type_model(Music, return_id=True), delete_object=True))


    def has_object_permission(self, request, view, obj):
        # only admin of channels can view unpublished musics
        if not obj.is_published:
            return (request.user.channel_admins.filter(channel=obj.channel).first())
        
        return True