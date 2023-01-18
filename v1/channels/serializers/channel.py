from rest_framework import serializers
from channels.models import Channel


class ChannelListSerializer(serializers.ModelSerializer):
    # TODO get subs count
    # TODO Add user role in channel
    class Meta:
        model = Channel
        fields = ["profile", "title", "token", "is_verified"]