from rest_framework.permissions import BasePermission
from core.models import ContentVisibility


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
        

class UpdateVideoPermission(BasePermission):
    message = 'Only channel admins can update videos.'

    def has_permission(self, request, view):
        """
        Check if user has permission to update video.
        """
        channel = view.channel
        user = request.user
        # Check if user is admin of channel
        admin = user.channel_admins.filter(channel=channel).first()
        return admin.permissions.can_edit_object


class DeleteVideoPermission(BasePermission):
    message = 'Only channel admins can delete videos.'

    def has_permission(self, request, view):
        """
        Check if user has permission to delete video.
        """
        channel = view.channel
        user = request.user
        # Check if user is admin of channel
        admin = user.channel_admins.filter(channel=channel).first()
        return admin.permissions.can_delete_object


class RetrievePrivateVideoPermission(BasePermission):
    message = 'Only channel admins can view private videos.'

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to view private video.
        """
        channel = view.channel
        return (
                obj.visibility == ContentVisibility.PUBLISHED or
                request.user.channel_admins.filter(channel=channel).exists()
        )
