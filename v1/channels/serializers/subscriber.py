from rest_framework import serializers
from channels.models import ChannelSubscriber


class SubscriberListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    channel_token = serializers.SerializerMethodField(method_name="get_channel_token")

    class Meta:
        model = ChannelSubscriber
        fields = ["user", "date", "channel_token"]

    def get_channel_token(self, obj):
        return obj.channel.token