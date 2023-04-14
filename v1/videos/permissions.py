from rest_framework.permissions import BasePermission

class CreateVideoPermission(BasePermission):
    message = 'You are not allowed to add video to this channel'

    def has_permission(self, request, view):
        channel = view.channel
        
        if request.method == "POST":
            if (admin:=channel.admins.filter(user=request.user).first()):
                # TODO update this and add model
                return (admin and admin.permissions.filter(add_object=True))
        
        return True
        

class VideoPermission(BasePermission):
    message = 'Permission denied.'
    
    def has_permission(self, request, view):

        # the given object
        object = view.get_object()

        admin = request.user.channel_admins.filter(channel=object.channel).first()

        # only channel owner and some admins can update a video
        if request.method in ["PUT", "PATCH"]:
            return (admin and admin.permissions.filter(model=object.get_model_content_type(), edit_object=True))


        # only channel owner and some admins can delete a video
        elif request.method == "DELETE":
            return (admin and admin.permissions.filter(model=object.get_model_content_type(), delete_object=True))

        return True

    def has_object_permission(self, request, view, obj):

        if not obj.is_published:
            return (request.user.channel_admins.filter(channel=obj.channel).first())
        
        return True