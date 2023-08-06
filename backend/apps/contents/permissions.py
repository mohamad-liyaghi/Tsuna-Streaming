from rest_framework.permissions import BasePermission
from contents.models import ContentVisibility


class CreateContentPermission(BasePermission):
    message = 'You dont have permission to add content'

    def has_permission(self, request, view):
        """
        Check if user has permission to add content.
        """
        channel = view.channel

        # Check if user is admin of channel
        admin = request.user.channel_admins.filter(channel=channel).first()
        return admin.permissions.can_add_object


class UpdateContentPermission(BasePermission):
    message = 'You dont have permission to update this object.'

    def has_permission(self, request, view):
        """
        Check if user has permission to update object.
        """
        channel = view.channel
        # Check if user is admin of channel
        admin = request.user.channel_admins.filter(channel=channel).first()
        return admin.permissions.can_edit_object


class DeleteContentPermission(BasePermission):
    message = 'You dont have permission to delete this content.'

    def has_permission(self, request, view):
        """
        Check if user has permission to delete object.
        """
        channel = view.channel
        # Check if user is admin of channel
        admin = request.user.channel_admins.filter(channel=channel).first()
        return admin.permissions.can_delete_object


class RetrievePrivateContentPermission(BasePermission):
    message = 'You dont have permission to retrieve private contents.'

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to view private objects.
        """
        channel = view.channel
        return (
                obj.visibility == ContentVisibility.PUBLISHED or
                request.user.channel_admins.filter(channel=channel).exists()
        )
