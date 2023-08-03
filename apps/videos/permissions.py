from rest_framework.permissions import BasePermission
from videos.models import Video
from core.utils import get_content_type_model


class CreateVideoPermission(BasePermission):
    message = 'Only channel admins can add videos.'

    def has_permission(self, request, view):
        """
        Check if user has permission to add video.
        """
        channel = view.channel
        user = request.user
        # Check if user is admin of channel
        admin = user.channel_admins.filter(channel=channel).first()
        return admin.permissions.can_add_object
        

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