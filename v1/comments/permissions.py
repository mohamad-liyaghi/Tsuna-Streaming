from rest_framework.permissions import BasePermission

class CommentPermission(BasePermission):
    
    message = 'Comments are closed.'

    def has_permission(self, request, view):

        object = view.object

        # users cannot add comment when allow_comment is False
        if request.method == "POST":
            return object.allow_comment

        return True
    


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
                admin = request.user.admin.filter(channel=object.content_object.channel).first()

                if admin:
                    # if user is admin, check if user has permission to delete comment.
                    if admin.permissions.filter(
                            model=object.get_model_content_type,
                            channel=object.content_object.channel,
                            delete_object_comment=True):
                        
                        return True
                    
                    return False
                
                return False
                

        return True