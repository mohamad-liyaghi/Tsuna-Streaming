from rest_framework.permissions import BasePermission
from videos.models import Video
from core.utils import get_content_type_model


class CreateVideoPermission(BasePermission):
    message = 'You are not allowed to add video to this channel'

    def has_permission(self, request, view):
        channel = view.channel
        
        if request.method == "POST":
            # Check if user is admin
            if (admin:=channel.admins.filter(user=request.user).first()):
                # If user is admin, check if user has permission to add video
                return (admin and admin.permissions.filter(model=get_content_type_model(Video), add_object=True))
            
            return False
        
        return True
        

class VideoPermission(BasePermission):
    message = 'Permission denied.'
    
    def has_permission(self, request, view):

        if request.method == "GET":
            return True
        
        admin = request.user.channel_admins.filter(channel=view.channel).first()

        # only channel owner and some admins can update a video
        if request.method in ["PUT", "PATCH"]:
            return (admin and admin.permissions.filter(model=get_content_type_model(Video), edit_object=True))


        # only channel owner and some admins can delete a video
        elif request.method == "DELETE":
            return (admin and admin.permissions.filter(model=get_content_type_model(Video), delete_object=True))


    def has_object_permission(self, request, view, obj):
        # only admin of channels can view unpublished videos
        if not obj.is_published:
            return (request.user.channel_admins.filter(channel=obj.channel).first())
        
        return True