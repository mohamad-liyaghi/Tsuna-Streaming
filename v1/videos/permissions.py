from rest_framework.permissions import BasePermission
from channels.models import ChannelAdmin

class VideoPermission(BasePermission):
    
    def has_permission(self, request, view):
        object = view.get_object()
        # only channel owner and some admins can update a video
        if request.method in ["PUT", "PATCH"]:
            if request.user == object.channel.owner or\
                ChannelAdmin.objects.filter(user=request.user, channel=object.channel, 
                            edit_video=True).exists():
                return True
            return False

        # only channel owner and some admins can delete a video
        elif request.method == "DELETE":
            if request.user == object.channel.owner or\
                ChannelAdmin.objects.filter(user=request.user, channel=object.channel, 
                                        delete_video=True).exists():
                return True
            return False

        return True

    def has_object_permission(self, request, view, obj):
        self.object = obj

        if obj.is_published:
            return True
        
        else:
            if request.user == obj.channel.owner or \
                ChannelAdmin.objects.filter(user=request.user, channel=obj.channel).exists():
                return True

            return False