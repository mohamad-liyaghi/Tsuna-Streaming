from rest_framework.permissions import BasePermission


class VideoPermission(BasePermission):
    message = 'Permission denied to access this video.'
    
    def has_permission(self, request, view):
        object = view.get_object()
        admin = request.user.channel_admin.filter(channel=object.channel).first()

        # only channel owner and some admins can update a video
        if request.method in ["PUT", "PATCH"]:
            return (admin and admin.edit_video)


        # only channel owner and some admins can delete a video
        elif request.method == "DELETE":
            return (admin and admin.delete_video)

        return True

    def has_object_permission(self, request, view, obj):

        if not obj.is_published:
            return (request.user.channel_admin.filter(channel=obj.channel).exists())
        
        return True