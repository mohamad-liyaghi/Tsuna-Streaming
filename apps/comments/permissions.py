from rest_framework.permissions import BasePermission
from core.utils import get_content_type_model


class CommentCreatePermission(BasePermission):
    
    message = 'Comments are not allowed for this object.'

    def has_permission(self, request, view):
        """
        Check if comments are allowed for an object.
        """
        return view.get_object().allow_comment
    


class CommentDetailPermission(BasePermission):
    message = 'You are not author of this comment.'
    
    def has_permission(self, request, view):
        object = view.get_object()

        if request.method in ["PUT", "PATCH"]:
            return (request.user == object.user)
        
        elif request.method == "DELETE":
            '''Object owner and channel admins can delete a comment.'''

            if request.user == object.user:
                return True
            
            else:
                # check if user is admin
                admin = request.user.channel_admins.filter(channel=object.content_object.channel).first()

                if admin:
                    # if user is admin, check if user has permission to delete comment.
                    if admin.permissions.filter(
                            model=get_content_type_model(model=self.__class__),
                            channel=object.content_object.channel,
                            delete_object_comment=True):
                        
                        return True
                    
                    return False
                
                return False
                

        return True