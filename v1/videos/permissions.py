from rest_framework.permissions import BasePermission


class VideoPermission(BasePermission):
    
    def has_permission(self, request, view):
        object = view.get_object()
        # only channel owner and some admins can update a video
        if request.method in ["PUT", "PATCH"]:
            if request.user.channel_admin.filter(channel=object.channel, edit_video=True).exists():
                return True
            return False

        # only channel owner and some admins can delete a video
        elif request.method == "DELETE":
            if request.user.channel_admin.filter(channel=object.channel, delete_video=True).exists():
                return True
            return False

        return True

    def has_object_permission(self, request, view, obj):
        self.object = obj

        if obj.is_published:
            return True
        
        else:
            if  request.user.channel_admin.filter(channel=obj.channel).exists():
                return True

            return False