from rest_framework.permissions import BasePermission

class CommentPermission(BasePermission):
    
    message = 'Comments are closed.'

    def has_permission(self, request, view):

        object = view.object

        # users cannot add comment when allow_comment is False
        if request.method == "POST":
            return object.allow_comment

        return True