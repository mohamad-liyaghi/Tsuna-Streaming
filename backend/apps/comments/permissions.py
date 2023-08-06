from rest_framework.permissions import BasePermission
from core.utils import get_content_type_model


class CommentCreatePermission(BasePermission):
    
    message = 'Comments are not allowed for this object.'

    def has_permission(self, request, view):
        """
        Check if comments are allowed for an object.
        """
        return view.get_object().allow_comment
    


class IsCommentOwner(BasePermission):
    """
    Check if user is the comment's owner.
    """

    message = 'You are not the owner of this comment.'

    def has_object_permission(self, request, view, obj):
        """
        Check if user is the comment's owner.
        For deleting, the content's channel admin can also delete the comment.
        """
        user = request.user
        match request.method:
            case 'PATCH' | 'PUT':
                return obj.user == user

            case 'DELETE':
                channel_admin = user.channel_admins.filter(
                    channel=obj.content_object.channel
                ).exists()
                return obj.user == user or channel_admin

class CanPinComment(BasePermission):
    """
    Check if user is the channel's admin.
    """

    message = 'You are not the channel admin.'

    def has_object_permission(self, request, view, obj):
        """
        Check if user is the channel's admin.
        """
        user = request.user
        # Check if user is the channel's admin.
        return user.channel_admins.filter(
            channel=obj.content_object.channel
        ).exists()
