from rest_framework.permissions import BasePermission


class VideoPermission(BasePermission):
    message = 'Permission denied.'
    
    def has_permission(self, request, view):

        # the given object
        object = view.get_object()

        admin = request.user.channel_admins.filter(channel=object.channel).first()

        # only channel owner and some admins can update a video
        if request.method in ["PUT", "PATCH"]:
            return (admin and admin.permissions.filter(model=object.get_model_content_type, edit_object=True))


        # only channel owner and some admins can delete a video
        elif request.method == "DELETE":
            return (admin and admin.permissions.filter(model=object.get_model_content_type, delete_object=True))

        return True

    def has_object_permission(self, request, view, obj):

        if not obj.is_published:
            return (request.user.channel_admins.filter(channel=obj.channel).first())
        
        return True