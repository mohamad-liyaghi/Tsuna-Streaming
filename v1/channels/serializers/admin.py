from rest_framework import serializers
from channels.models import ChannelAdmin

class ChannelAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = ["user", "date", "token"]


class ChannelAdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = ["user", "change_channel_info", "add_new_admin", "add_video",
                     "edit_video", "delete_video", "publish_video"]


class ChannelAdminDetailView(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = ["user", "change_channel_info", "add_new_admin", "add_video",
                     "edit_video", "delete_video", "publish_video"]