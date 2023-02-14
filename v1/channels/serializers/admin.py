from django.core.exceptions import ValidationError
from rest_framework import serializers
from channels.models import ChannelAdmin

class ChannelAdminListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
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
            try:
                return super().save(**kwargs)

            # raise a ValidationError when a user hasnt subscribed to channel and is getting promoted
            except ValidationError: 
                raise serializers.ValidationError("User hasnt subscribed to the channel.")
            
            # raise a ValueError when admin already exists
            except ValueError:
                raise serializers.ValidationError("Admin already exists.")

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