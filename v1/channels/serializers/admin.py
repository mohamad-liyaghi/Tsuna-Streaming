from rest_framework import serializers
from channels.models import ChannelAdmin

class ChannelAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = ["user", "date", "token"]


class ChannelAdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = [
            "user", 
            "change_channel_info", 
            "add_new_admin", 
            "add_video",
            "edit_video", 
            "delete_video", 
            "publish_video"
            ]


    def save(self, **kwargs):
        user = kwargs['promoted_by']
        channel = kwargs['channel']

        # check if user can add add admin
        request_admin = user.channel_admin.filter(
            channel=channel, add_new_admin=True
        ).first()

        if user == channel.owner or request_admin:
            return super().save(**kwargs)

        raise serializers.ValidationError("User doesnt have permission to promote admins.")


class ChannelAdminDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ChannelAdmin
        fields = ["user", "change_channel_info", "add_new_admin", "add_video",
                     "edit_video", "delete_video", "publish_video"]
        extra_kwargs = {
            "user" : {"read_only" : True},
        }